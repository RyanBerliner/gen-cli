" Ask questions about a file, or a selection in visual mode
nnoremap <C-g> :w !gen "
vnoremap <C-g> :w !gen "" -c %<Left><Left><Left><Left><Left><Left>

" Replace the entire file (upon confirming the diff), or replace just the
" selection in visual mode. Yes, this overrides Ctrl-c ... map to whatever
" you'd like.
nnoremap <C-c> :!gen -e "" %<Left><Left><Left>
vnoremap <C-c> :!gen "" -c %<Left><Left><Left><Left><Left><Left>
