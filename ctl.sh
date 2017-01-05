#!/bin/bash
# 
# django run by uwsgi with supervisor
# 2017/1/5

# default src path
source_path='/opt/asset/latest'

function do_c(){
    cd "${source_path}/www"
    ${PY27} manage.py collectstatic --no-input
}

function do_t(){
    cd "${source_path}/www"
    ${PY27} manage.py test
}

function do_r(){
    chown nobody:nobody -R "${source_path}/www"
    supervisorctl status
    supervisorctl reload
    sleep 2
    supervisorctl status
}

function usage(){
    cat <<_EOF

USAGE: $0 [c|f|r|t] [src_path]

    c  :     collectstatic
    r  :     reload supervisor
    t  :     test

    src_path : default: ${source_path}
_EOF
}

case $1 in
    c|r|t)
        PATH=$PATH:/usr/local/sbin:/usr/local/bin && export PATH
        python -c 'import sys;print sys.version' |grep '2.7' && PY27='python' || PY27='python2.7'
        ${PY27} -c 'import sys;print sys.version' 
        [ -z $2 ] || source_path=$2
        do_$1
        ;;
    *)
        usage
        ;;
esac
