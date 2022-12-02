(load "utils")
(defparameter ifile "./day01input.txt")

(defun 2sum (lst sum)
  (do* ((mp (make-hash-table))
        (l lst (cdr l))
        (match nil (gethash (car l) mp)))
    ((or (not (null match)) (null l))
     (if match 
         (list match (car l))
         nil))
    (setf (gethash (- sum (car l)) mp) (car l))))

(defun 3sum (lst sum)
  (some (lambda (curr) 
          (let ((2sum-res (2sum lst (- sum curr))))
            (if 2sum-res
                (cons curr 2sum-res)
                nil)))
        lst))

(defun solution-part-1 (lst)
  (let ((res (2sum lst 2020)))
    (if res
        (* (car res) (cadr res))
        nil)))
        
(defun solution-part-2 (lst)
  (let ((res (3sum lst 2020)))
    (if res
        (* (car res) (cadr res) (caddr res))
        nil)))

(format t "Part 1: ~A~%" (solution-part-1 (load-input ifile)))
(format t "Part 2: ~A~%" (solution-part-2 (load-input ifile)))
