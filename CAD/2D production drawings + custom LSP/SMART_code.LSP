;; _________________________________________________________________
(defun c:SMART_LNFT ()
  ;; Start debug
  (princ "\n[DEBUG 1] Function started.")

  ;; Prompt user to select multiple lines, arcs, or polylines to join
  (setq ss (ssget '((0 . "LINE,LWPOLYLINE,ARC,POLYLINE"))))  ; Allows selection of lines, polylines, and arcs
  (if ss
    (progn
      (princ "\n[DEBUG 2] Selection set created.")

      ;; Use PEDIT in multiple mode to join all selected lines into a polyline
      (command "_PEDIT" "_M" ss "" "_Y" "_JOIN" "" "")
      (princ "\n[DEBUG 3] All lines joined successfully.")

      ;; Get the joined polyline entity (the last entity created)
      (setq joinedEntity (entlast))

      ;; Check if a valid polyline entity was created
      (if (and joinedEntity (eq (cdr (assoc 0 (entget joinedEntity))) "LWPOLYLINE"))
        (progn
          ;; Get the total length of the joined polyline
          (setq len (vlax-curve-getDistAtParam joinedEntity (vlax-curve-getEndParam joinedEntity)))
          (princ (strcat "\n[DEBUG 4] Length of joined polyline: " (rtos len 2 2)))

          ;; Convert the length to feet and format with "LNFT" to one decimal place
          (setq length_in_feet (/ len 12))
          (setq length_str (strcat (rtos length_in_feet 2 1) " LNFT"))  ;; Adjusted to 1 decimal place
          (princ (strcat "\n[DEBUG 5] Length in feet with units: " length_str))

          ;; Prompt user for a point to place the length text
          (setq pt (getpoint "\nSelect point for length text: "))
          (princ "\n[DEBUG 6] Point selected for text placement.")

          ;; Place the length as text at the specified point
          (command "_MTEXT" pt "J" "MC" "W" 0.0 length_str "")
          (princ "\n[DEBUG 7] MText command executed.")
        )
        ;; Error handling if polyline creation fails
        (princ "\n[ERROR] Could not create a polyline. Please ensure valid entities are selected.")
      )
    )
    ;; Error handling for empty selection
    (princ "\n[ERROR] No valid entities selected.")
  )

  (princ "\n[DEBUG 8] Function completed.")  ; Exit quietly
)

;; _________________________________________________________________
(defun c:SMART_SQFT ()
  ;; Start debug
  (princ "\n[DEBUG 1] Function started.")

  ;; Prompt user to select multiple lines, arcs, or polylines to join
  (setq ss (ssget '((0 . "LINE,LWPOLYLINE,ARC,POLYLINE"))))  ; Allows selection of lines, polylines, and arcs
  (if ss
    (progn
      (princ "\n[DEBUG 2] Selection set created.")

      ;; Use PEDIT in multiple mode to join all selected lines into a polyline
      (command "_PEDIT" "_M" ss "" "_Y" "_JOIN" "" "")
      (princ "\n[DEBUG 3] All lines joined successfully.")

      ;; Get the joined polyline entity (the last entity created)
      (setq joinedEntity (entlast))

      ;; Check if a valid polyline entity was created
      (if (and joinedEntity (eq (cdr (assoc 0 (entget joinedEntity))) "LWPOLYLINE"))
        (progn
          ;; Get the area of the joined polyline
          (setq area (vlax-get-property (vlax-ename->vla-object joinedEntity) 'Area))
          (princ (strcat "\n[DEBUG 4] Area of joined polyline: " (rtos area 2 2)))

          ;; Convert the area to square feet and format with "SQFT"
          (setq area_in_sqft (/ area 144))
          (setq area_str (strcat (rtos area_in_sqft 2 1) " SQFT"))  ;; Adjusted to 1 decimal place
          (princ (strcat "\n[DEBUG 5] Area in square feet with units: " area_str))

          ;; Prompt user for a point to place the area text
          (setq pt (getpoint "\nSelect point for area text: "))
          (princ "\n[DEBUG 6] Point selected for text placement.")

          ;; Place the area as text at the specified point
          (command "_MTEXT" pt "J" "MC" "W" 0.0 area_str "")
          (princ "\n[DEBUG 7] MText command executed.")
        )
        ;; Error handling if polyline creation fails
        (princ "\n[ERROR] Could not create a polyline. Please ensure valid entities are selected and joined properly.")
      )
    )
    ;; Error handling for empty selection
    (princ "\n[ERROR] No valid entities selected.")
  )

  (princ "\n[DEBUG 8] Function completed.")  ; Exit quietly
)

;; _________________________________________________________________
(defun c:SMART_Numbering ()
  ;; Initialize the counter starting at 1
  (setq count 1)

  ;; Loop until the user presses Enter or Escape
  (while T
    ;; Create the text string with the current count
    (setq text_str (strcat "# " (itoa count)))

    ;; Prompt user to click to place the text
    (setq pt (getpoint "\nClick to place text, or press Enter/ESC to exit: "))

    ;; Exit the loop if Enter or Escape is pressed
    (if (not pt)
      (exit)  ; Exit the loop and function
    )

    ;; Place the text at the specified point with a height of 2.5
    (command "_MTEXT" pt "J" "MC" "H" 2.5 "W" 0.0 text_str "")

    ;; Increment the counter for the next placement
    (setq count (1+ count))
  )
  (princ)  ; Exit quietly
)

;; _________________________________________________________________
(defun c:SMART_UPDATE_1 ()
  (princ "\n[DEBUG] SMART_UPDATE function started.")

  ;; Define table handles by converting each handle directly into a table object
  (setq model-project-table (vlax-ename->vla-object (handent "777c")))
  (setq model-area-table (vlax-ename->vla-object (handent "796d")))
  (setq paper-project-table (vlax-ename->vla-object (handent "7be1")))
  (setq paper-area-table (vlax-ename->vla-object (handent "7b4a")))

  ;; Validate that all table objects were found
  (if (and model-project-table model-area-table paper-project-table paper-area-table)
    (progn
      (princ "\n[DEBUG] All tables found. Starting data transfer.")

      ;; Project Table Transfer - straightforward copy of all cells
      (setq max-cols 7)  ; Set according to "Project Specific Data" table structure
      (setq max-rows 3)
      (setq row 0)
      (while (< row max-rows)
        (setq col 0)
        (while (< col max-cols)
          ;; Get and transfer cell text
          (setq cell-value (vla-getText model-project-table row col))
          (if cell-value
            (progn
              (vla-setText paper-project-table row col cell-value)
              (princ (strcat "\n[DEBUG] Updated project target table cell (" (itoa row) ", " (itoa col) ") with value: " cell-value))
            )
          )
          (setq col (1+ col))
        )
        (setq row (1+ row))
      )

      ;; Area Table Transfer - Copy columns based on header presence
      (setq max-cols 9)  ; Adjust to max columns in "Area Specific Data" table
      (setq row-start 2)  ; Start from row 3, following headers in row 2
      (setq max-rows 15)
      (setq col 1)  ; Start from column B

      (while (< col max-cols)
        ;; Check if the header cell in row 3 is populated
        (setq header-value (vla-getText model-area-table 2 col))
        (if (and header-value (/= header-value ""))  ; Header exists
          (progn
            (princ (strcat "\n[DEBUG] Starting updates for column " (itoa col) ". Header: " header-value))
            ;; Loop through rows from 3 to 16 to transfer data
            (setq row row-start)
            (while (<= row max-rows)
              ;; Get cell value from model table and update in paper table
              (setq cell-value (vla-getText model-area-table row col))
              (vla-setText paper-area-table row col cell-value)
              (princ (strcat "\n[DEBUG] Updated area target table cell (" (itoa row) ", " (itoa col) ") with value: " cell-value))
              (setq row (1+ row))
            )
          )
          ;; Stop if column header is empty
          (princ (strcat "\n[INFO] Stopping updates at column " (itoa col) " due to empty header."))
        )
        (setq col (1+ col))
      )

      (princ "\n[INFO] Data transferred successfully from Model Space to Paper Space tables.")
    )
    (progn
      ;; Error messages if table handles are not found
      (if (not model-project-table) (princ "\n[ERROR] Model Project table handle not found."))
      (if (not model-area-table) (princ "\n[ERROR] Model Area table handle not found."))
      (if (not paper-project-table) (princ "\n[ERROR] Paper Project table handle not found."))
      (if (not paper-area-table) (princ "\n[ERROR] Paper Area table handle not found."))
      (princ "\n[ERROR] Data transfer failed. Check table handles and try again.")
    )
  )

  (princ "\n[DEBUG] Function completed.")
)

;; _________________________________________________________________

(defun c:SMART_UPDATE ()
  (princ "\n[DEBUG] SMART_UPDATE function started.")

  ;; Define table handles by converting each handle directly into a table object
  (setq model-project-table (vlax-ename->vla-object (handent "777c")))
  (setq model-area-table (vlax-ename->vla-object (handent "796d")))
  (setq paper-project-table (vlax-ename->vla-object (handent "7be1")))
  (setq paper-area-table (vlax-ename->vla-object (handent "7b4a")))

  ;; Validate that all table objects were found
  (if (and model-project-table model-area-table paper-project-table paper-area-table)
    (progn
      (princ "\n[DEBUG] All tables found. Starting data transfer.")

      ;; Project Table Transfer - straightforward copy of all cells
      (setq max-cols 7)  ; Set according to "Project Specific Data" table structure
      (setq max-rows 3)
      (setq row 0)
      (while (< row max-rows)
        (setq col 0)
        (while (< col max-cols)
          ;; Get and transfer cell text
          (setq cell-value (vla-getText model-project-table row col))
          (if cell-value
            (progn
              (vla-setText paper-project-table row col cell-value)
              (princ (strcat "\n[DEBUG] Updated project target table cell (" (itoa row) ", " (itoa col) ") with value: " cell-value))
            )
          )
          (setq col (1+ col))
        )
        (setq row (1+ row))
      )

      ;; Area Table Transfer - Copy columns based on header presence
      (setq max-cols 10)  ; Adjust to max columns in "Area Specific Data" table
      (setq row-start 2)  ; Row 2 (header row)
      (setq max-rows 15)  ; Adjusted to 15 to correctly index up to the 16th row
      (setq col 1)  ; Start from column B

      (while (< col max-cols)
        ;; Check if the header cell in row 3 is populated
        (setq header-value (vla-getText model-area-table row-start col))
        (if (and header-value (/= header-value ""))  ; Header exists
          (progn
            (princ (strcat "\n[DEBUG] Starting updates for column " (itoa col) ". Header: " header-value))
            ;; Update header cell in the target table first
            (vla-setText paper-area-table row-start col header-value)
            ;; Loop through rows from 3 to 15 to transfer data
            (setq row (1+ row-start))
            (while (<= row max-rows)
              ;; Get cell value from model table and update in paper table
              (setq cell-value (vla-getText model-area-table row col))
              (condition-case err
                (progn
                  ;; Handle each cell, even if it's blank
                  (if cell-value
                    (vla-setText paper-area-table row col cell-value)
                    (vla-setText paper-area-table row col "")
                  )
                  (princ (strcat "\n[DEBUG] Updated area target table cell (" (itoa row) ", " (itoa col) ") with value: " cell-value))
                )
                (error
                  (princ (strcat "\n[ERROR] Failed to update cell at (" (itoa row) ", " (itoa col) "). Skipping."))
                )
              )
              (setq row (1+ row))
            )
          )
          ;; Log message if column is skipped due to an empty header
          (princ (strcat "\n[INFO] Skipping column " (itoa col) " due to empty header in model table."))
        )
        (setq col (1+ col))
      )

      (princ "\n[INFO] Data transferred successfully from Model Space to Paper Space tables.")
    )
    (progn
      ;; Error messages if table handles are not found
      (if (not model-project-table) (princ "\n[ERROR] Model Project table handle not found."))
      (if (not model-area-table) (princ "\n[ERROR] Model Area table handle not found."))
      (if (not paper-project-table) (princ "\n[ERROR] Paper Project table handle not found."))
      (if (not paper-area-table) (princ "\n[ERROR] Paper Area table handle not found."))
      (princ "\n[ERROR] Data transfer failed. Check table handles and try again.")
    )
  )

  (princ "\n[DEBUG] Function completed.")
)

;; _________________________________________________________________

(defun c:SMART_DIMS ()
  (princ "\n[DEBUG] SMART_DIMS function started.")

  ;; Prompt user to select objects
  (setq ss (ssget))
  (if ss
    (progn
      ;; Initialize points list and variables for max/min coordinates
      (setq points '() max_x nil max_y nil min_x nil min_y nil)

      ;; Collect points from selected entities and determine Min/Max X and Y
      (setq i 0)
      (while (< i (sslength ss))
        (setq ent (ssname ss i))
        (setq entData (vlax-ename->vla-object ent))
        
        ;; Process only line or polyline entities
        (if (or (= (vla-get-ObjectName entData) "AcDbLine")
                (= (vla-get-ObjectName entData) "AcDbPolyline"))
          (progn
            ;; For a line, get start and end points
            (if (= (vla-get-ObjectName entData) "AcDbLine")
              (setq points (append points (list (vlax-get entData 'StartPoint) (vlax-get entData 'EndPoint))))
            )
            ;; For a polyline, get all vertex points
            (if (= (vla-get-ObjectName entData) "AcDbPolyline")
              (progn
                (setq numVerts (vlax-get entData 'NumberOfVertices))
                (setq v 0)
                (while (< v numVerts)
                  (setq pt (vlax-get entData 'Coordinates v))
                  (setq points (append points (list pt)))
                  (setq v (1+ v))
                )
              )
            )
          )
        )
        (setq i (1+ i))
      )

      ;; Find max/min X and Y coordinates across all points
      (foreach pt points
        (setq x (car pt) y (cadr pt))
        (if (or (not max_x) (> x max_x)) (setq max_x x))
        (if (or (not min_x) (< x min_x)) (setq min_x x))
        (if (or (not max_y) (> y max_y)) (setq max_y y))
        (if (or (not min_y) (< y min_y)) (setq min_y y))
      )

      ;; Identify each corner using the equations provided
      (setq sw-check -999999 se-check -999999 nw-check -999999 ne-check -999999)  ; Initialize checks

      ;; Loop to evaluate each point for corner checks
      (foreach pt points
        (setq x (car pt) y (cadr pt))
        
        ;; Calculate checks based on provided formulas
        (setq sw-value (+ (- max_x x) (- max_y y)))
        (setq se-value (+ (- x min_x) (- max_y y)))
        (setq nw-value (+ (- max_x x) (- y min_y)))
        (setq ne-value (+ (- x min_x) (- y min_y)))

        ;; Determine if point qualifies as each corner
        (if (> sw-value sw-check)
          (progn (setq sw-corner pt) (setq sw-check sw-value)))
        (if (> se-value se-check)
          (progn (setq se-corner pt) (setq se-check se-value)))
        (if (> nw-value nw-check)
          (progn (setq nw-corner pt) (setq nw-check nw-value)))
        (if (> ne-value ne-check)
          (progn (setq ne-corner pt) (setq ne-check ne-value)))
      )

      ;; Debug output of calculated corner points
      (princ (strcat "\n[DEBUG] North-West corner: " (vl-prin1-to-string nw-corner)))
      (princ (strcat "\n[DEBUG] North-East corner: " (vl-prin1-to-string ne-corner)))
      (princ (strcat "\n[DEBUG] South-West corner: " (vl-prin1-to-string sw-corner)))
      (princ (strcat "\n[DEBUG] South-East corner: " (vl-prin1-to-string se-corner)))

      ;; Add dimensions between these corner points
      ;; Dimension from North-West to North-East (Horizontal)
      (command "_.DIMHORIZONTAL" nw-corner ne-corner (polar nw-corner (/ pi 2) 4))
      (princ "\n[DEBUG] Horizontal dimension added from North-West to North-East.")

      ;; Dimension from North-East to South-East (Vertical)
      (command "_.DIMVERTICAL" ne-corner se-corner (polar ne-corner 0 4))
      (princ "\n[DEBUG] Vertical dimension added from North-East to South-East.")

      ;; Dimension from South-East to South-West (Horizontal)
      (command "_.DIMHORIZONTAL" se-corner sw-corner (polar se-corner (/ (* 3 pi) 2) 4))
      (princ "\n[DEBUG] Horizontal dimension added from South-East to South-West.")

      ;; Dimension from South-West to North-West (Vertical)
      (command "_.DIMVERTICAL" sw-corner nw-corner (polar sw-corner pi 4))
      (princ "\n[DEBUG] Vertical dimension added from South-West to North-West.")

      (princ "\n[INFO] Dimensions added successfully.")
    )
    (princ "\n[ERROR] No valid objects selected.")
  )

  (princ "\n[DEBUG] SMART_DIMS function completed.")
)

;; _________________________________________________________________

(defun parse-csv-line (line delimiter)
  "Splits a line of CSV text by the given delimiter and returns a list of cells."
  (setq cells '())
  (while line
    (setq pos (vl-string-search delimiter line))
    (if pos
      (progn
        (setq cell (substr line 1 pos))
        (setq line (substr line (+ pos 2)))
      )
      (progn
        (setq cell line)
        (setq line nil)
      )
    )
    ;; Remove leading and trailing whitespace
    (setq cell (vl-string-right-trim " " (vl-string-left-trim " " cell)))
    ;; Remove extraneous quotes around the cell
    (if (and (>= (strlen cell) 2) (equal (substr cell 1 1) "\"") (equal (substr cell (strlen cell)) "\""))
      (setq cell (substr cell 2 (- (strlen cell) 2)))
    )
    ;; Replace double quotes (if any) within cell content
    (setq cell (vl-string-subst "\"" "\"\"" cell))
    (setq cells (append cells (list cell)))
  )
  cells
)

(defun get-current-date ()
  "Returns the current date in MM.DD.YY format."
  (setq date (vl-string-right-trim " " (menucmd "m=$(edtime,$(getvar,date),MO.DD.YY)")))
  date
)

(defun c:SMART_TABLE ()
  (princ "\n[DEBUG] SMART_TABLE function started.")
  
  ;; Set initial path to the Downloads folder
  (setq initial-path "C:\\Users\\Admin\\Downloads\\")
  (setq file-path (getfiled "Select CSV File" initial-path "csv" 4))
  
  (if (not file-path)
    (progn
      (princ "\n[ERROR] No file selected.")
      (exit)
    )
  )

  ;; Attempt to open the selected CSV file for reading
  (setq csv-file (open file-path "r"))
  (if csv-file
    (progn
      (princ (strcat "\n[DEBUG] Opened CSV file at: " file-path))

      ;; Initialize an empty list to store each row's cells as sublists
      (setq data '())

      ;; Read and parse each line of the CSV
      (while (setq line (read-line csv-file))
        ;; Use custom parse function to split line by commas
        (setq cells (parse-csv-line line ","))
        
        ;; Debugging: Display each parsed line
        (princ (strcat "\n[DEBUG] Parsed line: " line))
        
        ;; Add parsed cells as a row in data
        (setq data (append data (list cells)))
      )

      ;; Close the file after reading
      (close csv-file)

      ;; Adjusted mappings of row-column indices to MText object handles
      (setq mappings '(((2 0) . "13fe") ((2 1) . "14a0") ((2 2) . "1416")
                       ((2 3) . "147c") ((2 4) . "148a") ((2 5) . "1426")
                       ((2 6) . "142c") ((5 1) . "1545") ((6 1) . "14bc")
                       ((7 1) . "14c2") ((8 1) . "14ac") ((9 1) . "14c8")
                       ((10 1) . "14d4") ((11 1) . "14b6") ((12 1) . "14a6")
                       ((13 1) . "14ce") ((14 1) . "154d") ((15 1) . "154a")
                       ((16 1) . "154b") ((17 1) . "154c")))

      ;; Process each mapping to update AutoCAD MText
      (foreach mapping mappings
        (setq row-col (car mapping))
        (setq row (car row-col))
        (setq col (cadr row-col))
        (setq handle (cdr mapping))

        ;; Check if row and column exist in data
        (if (and (nth row data) (nth col (nth row data)))
          (setq value (nth col (nth row data)))
          (setq value "")
        )

        ;; Add prefix for specific handle (e.g., "1416")
        (if (equal handle "1416")
          (setq value (strcat "PROCESSED BY: " value))
        )

        ;; Set current date for handle "14a0"
        (if (equal handle "14a0")
          (setq value (get-current-date))
        )

        ;; Find and update the MText object in AutoCAD
        (setq mtext-obj (vlax-ename->vla-object (handent handle)))
        (if mtext-obj
          (progn
            ;; Ensure quotation check is applied to all cells
            (if (and (>= (strlen value) 2) (equal (substr value 1 1) "\"") (equal (substr value (strlen value)) "\""))
              (setq value (substr value 2 (- (strlen value) 2)))
            )
            ;; Apply alignment: right for "1416" and centered for others
            (princ (strcat "\n[DEBUG] Updating MText handle " handle " with value: " value))
            (vla-put-TextString mtext-obj value)
            (if (equal handle "1416")
              (vla-put-AttachmentPoint mtext-obj acAttachmentPointMiddleRight)
              (vla-put-AttachmentPoint mtext-obj acAttachmentPointMiddleCenter)
            )
            ;; Set color to red for handle "1426"
            (if (equal handle "1426")
              (vla-put-Color mtext-obj 1)  ;; Color set to index 1 (Red)
            )
            (princ (strcat "\n[DEBUG] Updated MText handle " handle " successfully with value: " value))
          )
          (princ (strcat "\n[ERROR] MText handle " handle " not found."))))

      (princ "\n[INFO] Data transfer complete.")
    )
    (princ "\n[ERROR] Could not open CSV file. Check file path.")
  )

  (princ "\n[DEBUG] SMART_TABLE function completed.")
)
