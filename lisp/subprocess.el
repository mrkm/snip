;; Ruremaを検索
(defun rurema-which-one (num)
  "Select method number"
  (interactive "swhich-one?: ")
  (concat (format "%s" num) "\n"))
 
(defun rurema-filter (process string)
  "Rurema filter"
  (with-output-to-temp-buffer "*Help*" (princ string))
  (when (and (equal (process-status  process) 'run)
             (not (string-match "searching" string)))
             (process-send-string process (call-interactively 'rurema-which-one))))
 
 
(defun snip-search ()
  "execute snip"
  (interactive)
  (let (word)
    (setq word (if (and transient-mark-mode mark-active)
                   (buffer-substring-no-properties (region-beginning) (region-end))
                 (thing-at-point 'word)))
    (set-process-filter (start-process-shell-command
                         "snip"
                         "*snip*"
                         "snip"
                         word)
                        'rurema-filter)))
 
(defun rurema-search-word (word)
  "search method"
  (start-process-shell-command
   "rurema"
   "*ruby-refarence-manual*"
   "rurema"
   (concat (format "%s" word) "\n"))
  )

(add-hook 'ruby-mode-hook
          '(lambda ()
             (define-key ruby-mode-map (kbd "M-s") 'snip-search)
             ))
(defun rurema-search ()
  
)