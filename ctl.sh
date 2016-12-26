#!/bin/bash
# 
# 2016/12/26

# default src path
source_path='/opt/asset/latest'

function do_f(){
    n=`find "${source_path}/www" ! -user nobody -print |wc -l`
    if [ $n -eq 0 ]; then
        echo '[-] Up to date!'
    else
        echo '[-] List the files that should chown to nobody:'
        find "${source_path}/www" ! -user nobody -print
        chown nobody:nobody -R "${source_path}/www"
        do_r
    fi
}

function do_c(){
    cd "${source_path}/www"
    python manage.py collectstatic
}

function do_t(){
    cd "${source_path}/www"
    python manage.py test
}

function do_r(){
    /usr/local/bin/supervisorctl status
    /usr/local/bin/supervisorctl reload
    sleep 2
    /usr/local/bin/supervisorctl status
}

function usage(){
    cat <<_EOF

USAGE: $0 [c|f|r|t] [src_path]

    c  :     collectstatic
    f  :     chown to nobody and reload
    r  :     reload supervisor
    t  :     test

    src_path : default: ${source_path}
_EOF
}

case $1 in
    c|f|r|t)
        [ -z $2 ] || source_path=$2
        do_$1
        ;;
    *)
        usage
        ;;
esac
