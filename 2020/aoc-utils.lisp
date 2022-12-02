(defun load-input (path)
  (with-open-file (in path :direction :input)
    (let ((eof (list 'eof)))
      (do* ((line (read in nil eof)
                  (read in nil eof))
            (res (cons line nil)
                 (cons line res)))
        ((eql line eof) (nreverse (cdr res)))))))

