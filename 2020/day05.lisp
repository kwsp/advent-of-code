(load "aoc-utils")

(defparameter ifile "./day05input.txt")


(defun calc-row (s)
  (do ((low 0 (if (eql c #\B)
                  (1+ (floor (/ (+ high low) 2)))
                  low))
       (high 127 (if (eql c #\F)
                     (floor (/ (+ high low) 2))
                     high))
       (i 1 (1+ i))
       (c (char s 0) (char s i)))
      ((>= i 7)
       (if (eql c #\F) low high))))


(defun calc-col (s)
  (do ((low 0 (if (eql c #\R)
                  (ceiling (/ (+ high low) 2))
                  low))
       (high 7 (if (eql c #\L)
                   (floor (/ (+ high low) 2))
                   high))
       (i 8 (1+ i))
       (c (char s 7) (char s i)))
      ((>= i 10)
       (if (eql c #\L) low high))))

(defun calc-id (row col)
  (+ (* row 8) col))


(defun solution-part-1 (tickets)
  (do ((ll (cdr tickets) (cdr ll))
       (s (symbol-name (car tickets)) (symbol-name (car ll)))
       (col 0 (calc-col s))
       (row 0 (calc-row s))
       (max-id 0 (max max-id (calc-id row col))))
      ((null ll) max-id)))



(defun solution-part-2 (tickets)
  (find-missing (sort (calc-ticket-ids tickets) #'>)))

(defun find-missing (sorted-ids)
  (do ((ll (cdr sorted-ids) (cdr ll))
       (prev (car sorted-ids) curr)
       (curr (cadr sorted-ids) (car ll)))
      ((or (null ll)
           (= (+ curr 2) prev))
       (1- prev))))

(defun calc-ticket-ids (tickets)
  (do ((ll (cdr tickets) (cdr ll))
       (s (symbol-name (car tickets)) (symbol-name (car ll)))
       (col 0 (calc-col s))
       (row 0 (calc-row s))
       (ids nil (cons (calc-id row col) ids)))
      ((null ll) ids)))

(format t "Part 1: ~A~%" (solution-part-1 (load-input ifile)))
(format t "Part 2: ~A~%" (solution-part-2 (load-input ifile)))


(defun test-single (ticket row col id)
  (= row (calc-row ticket))
  (= col (calc-col ticket))
  (= id (calc-id row col)))

(defun test ()
  (test-single "BFFFBBFRRR" 70 7 567)
  (test-single "FBFBBFFRLR" 44 5 357)
  (test-single "FFFBBBFRRR" 14 7 119)
  (test-single "BBFFBBFRLL" 102 4 820)
  )

