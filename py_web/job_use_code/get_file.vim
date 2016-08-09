%s/\[\|\('\]\)\|\(u'\)//g
%s/', /\r/g
sort
g/^\(.*\)$\n\1/d
update
quit
