#!/bin/bash

# Determine basename and path of call
mypath="$( cd "$(dirname "$0")" ; pwd )"
myname=${0##*/}
envbin=$(which $myname)

# Remove current instance of wrapper from PATH, if set
if cmp --silent $envbin $mypath/$myname; then
    newpath=${PATH/${envbin%/*}:}

    if [[ $newpath == $PATH ]]; then
        echo "NCAR_ERROR: cannot remove wrapper from path"
        exit 1
    else
        export PATH=$newpath
    fi
fi

# Check for existence of actual binary
if ! which $myname >& /dev/null; then
    echo "NCAR_ERROR: wrapper cannot locate path to $myname"
    exit 1
fi

# Function to collect module settings from environment
function get_module_flags {
    vartype=$1 prefix=$2 rawlist="$3" varlist=
    [[ ${rawlist}z == z ]] && return

    if [[ $userank == true ]]; then
        for var in $rawlist; do
            rankvar=${var/NCAR_$vartype/NCAR_RANK}

            if [[ ${!rankvar}z != z ]]; then
                if [[ ${!rankvar} == *[!0-9]* ]]; then
                    echo "Warning: $rankvar is not an integer (${!rankvar})"
                    varlist="$varlist 0:$var"
                else
                    varlist="$varlist ${!rankvar}:$var"
                fi
            else
                varlist="$varlist 0:$var"
            fi
        done

        varlist=$(echo $varlist | xargs -n1 | sort -nr | cut -d: -f2 | xargs)
    else
        varlist=$rawlist
    fi

    for var in $varlist; do
        margs[$vartype]="${prefix}${!var} ${margs[$vartype]}"
    done
}

# Skip wrapper if it has already been called
if [[ $NCAR_WRAPPER_ACTIVE == true ]]; then
    # Preserve quotes from input arguments
    for arg in "$@"; do
        inargs+=("$arg")
    done

    $myname "${inargs[@]}"
else
    # Do we need to deal with ranking?
    if [[ -n ${!NCAR_RANK*} ]]; then
        userank=true
    fi

    # Associative storage for variables
    declare -A margs

    # Get any modifier flags that must go first
    if [[ " gcc g++ gfortran " != *" $myname "* ]]; then
        margs[MFLAGS]=$NCAR_MFLAGS_COMPILER
    fi

    # Add headers to compile line
    get_module_flags INC -I "${!NCAR_INC_*}"

    if [[ " $@ " != *" -c "* ]]; then
        # Add library paths to link line
        get_module_flags LDFLAGS -Wl,-rpath, "${!NCAR_LDFLAGS_*}"
        get_module_flags LDFLAGS -L "${!NCAR_LDFLAGS_*}"

        # Make sure RPATHs are respected by newer ldd
        margs[LDFLAGS]="-Wl,--disable-new-dtags ${margs[LDFLAGS]}"

        # Add library flags if desired
        if [[ -z ${NCAR_EXCLUDE_LIBS+x} ]]; then
            get_module_flags LIBS "" "${!NCAR_LIBS_*}"
        fi

        # Add asneeded unless disabled
        if [[ -z ${NCAR_EXCLUDE_ASNEEDED} ]]; then
            margs[LIBS]="-Wl,--as-needed ${margs[LIBS]}"
        fi
    fi

    # Process arguments and preserve "user" arg formatting
    userargs=()

    for arg in "$@"; do
        case "$arg" in
            --ncar-debug-include)
                echo ${margs[INC]}
                exit 0
                ;;
            --ncar-debug-libraries)
                echo ${margs[LIBS]} ${margs[LDFLAGS]}
                exit 0
                ;;
            --show)
                show=true
                ;;
            *)
                if [[ " ${margs[LIBS]} " != *" $arg "* ]]; then
                    userargs+=("$arg")
                fi
                ;;
        esac
    done

    # Call command with module and user args
    if [[ $show == true ]]; then
        if [[ $NCAR_WRAPPER_PREPEND_RPATH == true ]]; then
            echo "${myname} ${margs[MFLAGS]} ${margs[LDFLAGS]} ${userargs[@]} ${margs[INC]} ${margs[LIBS]}"
        else
            echo "${myname} ${margs[MFLAGS]} ${userargs[@]} ${margs[INC]} ${margs[LIBS]} ${margs[LDFLAGS]}"
        fi
    else
        export NCAR_WRAPPER_ACTIVE=true

        if [[ $NCAR_WRAPPER_PREPEND_RPATH == true ]]; then
            $myname ${margs[MFLAGS]} ${margs[LDFLAGS]} "${userargs[@]}" ${margs[INC]} ${margs[LIBS]}
        else
            $myname ${margs[MFLAGS]} "${userargs[@]}" ${margs[INC]} ${margs[LIBS]} ${margs[LDFLAGS]}
        fi
    fi
fi
