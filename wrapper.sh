#!/bin/bash

# Determine basename and path of call
MYPATH="$( cd "$(dirname "$0")" ; pwd )"
MYNAME=${0##*/}
ENVBIN=$(which $MYNAME)

# Remove current instance of wrapper from PATH, if set
if cmp --silent $ENVBIN $MYPATH/$MYNAME; then
    NEWPATH=${PATH/${ENVBIN%/*}:}

    if [[ $NEWPATH == $PATH ]]; then
        echo "NCAR_ERROR: cannot remove wrapper from path"
        exit 1
    else
        export PATH=$NEWPATH
    fi
fi

# Check for existence of actual binary
if ! which $MYNAME >& /dev/null; then
    echo "NCAR_ERROR: wrapper cannot locate path to $MYNAME"
    exit 1
fi

# Function to collect module settings from environment
function get_module_flags {
    VARTYPE=$1 PREFIX=$2 RAWLIST="$3" VARLIST=
    [[ ${RAWLIST}z == z ]] && return

    for VAR in $RAWLIST; do
        RANKVAR=${VAR/NCAR_$VARTYPE/NCAR_RANK}

        if [[ ${!RANKVAR}z != z ]]; then
            if [[ ${!RANKVAR} == *[!0-9]* ]]; then
                echo "Warning: $RANKVAR is not an integer (${!RANKVAR})"
                VARLIST="$VARLIST 0:$VAR"
            else
                VARLIST="$VARLIST ${!RANKVAR}:$VAR"
            fi
        else
            VARLIST="$VARLIST 0:$VAR"
        fi
    done

    VARLIST=$(echo $VARLIST | xargs -n1 | sort -nr | cut -d: -f2 | xargs)

    for VAR in $VARLIST; do
        MARGS[$VARTYPE]="${PREFIX}${!VAR} ${MARGS[$VARTYPE]}"
    done
}

# Skip wrapper if it has already been called
if [[ $NCAR_WRAPPER_ACTIVE == true ]]; then
    # Preserve quotes from input arguments
    for ARG in "$@"; do
        INARGS+=("$ARG")
    done

    $MYNAME "${INARGS[@]}"
else
    # Associative storage for variables
    declare -A MARGS

    # Add headers to compile line
    get_module_flags INC -I "${!NCAR_INC_*}"

    # Add library paths to link line
    get_module_flags LDFLAGS -Wl,-rpath, "${!NCAR_LDFLAGS_*}"
    get_module_flags LDFLAGS -L "${!NCAR_LDFLAGS_*}"

    # Get any modifier flags that must go first
    if [[ " gcc g++ gfortran " != *" $MYNAME "* ]]; then
        MARGS[MFLAGS]=$NCAR_MFLAGS_COMPILER
    fi

    # Make sure RPATHs are respected by newer ldd
    MARGS[LDFLAGS]="-Wl,--disable-new-dtags ${MARGS[LDFLAGS]}"

    # Add library flags if desired
    if [[ -z ${NCAR_EXCLUDE_LIBS+x} ]]; then
        get_module_flags LIBS "" "${!NCAR_LIBS_*}"
    fi

    # Add asneeded unless disabled
    if [[ -z ${NCAR_EXCLUDE_ASNEEDED} ]]; then
        MARGS[LIBS]="-Wl,--as-needed ${MARGS[LIBS]}"
    fi

    # Process arguments and preserve "user" arg formatting
    USERARGS=()

    for ARG in "$@"; do
        case "$ARG" in
            --ncar-debug-include)
                echo ${MARGS[INC]}
                exit 0
                ;;
            --ncar-debug-libraries)
                echo ${MARGS[LIBS]} ${MARGS[LDFLAGS]}
                exit 0
                ;;
            --show)
                SHOW=TRUE
                ;;
            *)
                if [[ " ${MARGS[LIBS]} " != *" $ARG "* ]]; then
                    USERARGS+=("$ARG")
                fi
                ;;
        esac
    done

    # Call command with module and user args
    if [[ $SHOW == TRUE ]]; then
        if [[ $NCAR_WRAPPER_PREPEND_RPATH == true ]]; then
            echo "${MYNAME} ${MARGS[MFLAGS]} ${MARGS[LDFLAGS]} ${USERARGS[@]} ${MARGS[INC]} ${MARGS[LIBS]}"
        else
            echo "${MYNAME} ${MARGS[MFLAGS]} ${USERARGS[@]} ${MARGS[INC]} ${MARGS[LIBS]} ${MARGS[LDFLAGS]}"
        fi
    else
        export NCAR_WRAPPER_ACTIVE=true

        if [[ $NCAR_WRAPPER_PREPEND_RPATH == true ]]; then
            $MYNAME ${MARGS[MFLAGS]} ${MARGS[LDFLAGS]} "${USERARGS[@]}" ${MARGS[INC]} ${MARGS[LIBS]}
        else
            $MYNAME ${MARGS[MFLAGS]} "${USERARGS[@]}" ${MARGS[INC]} ${MARGS[LIBS]} ${MARGS[LDFLAGS]}
        fi
    fi
fi
