if status is-interactive
    # Commands to run in interactive sessions can go here

set fish_greeting

neofetch | lolcat


set EDITOR "nvim -t -a ''"                 # $EDITOR use nvim in terminal
set -x PATH ~/miniforge3/bin/conda $PATH

# Swap between default and VI-style binds
function fish_user_key_bindings
  # fish_default_key_bindings
  fish_vi_key_bindings
end


### SPARK ###
set -g spark_version 1.0.0

complete -xc spark -n __fish_use_subcommand -a --help -d "Show usage help"
complete -xc spark -n __fish_use_subcommand -a --version -d "$spark_version"
complete -xc spark -n __fish_use_subcommand -a --min -d "Minimum range value"
complete -xc spark -n __fish_use_subcommand -a --max -d "Maximum range value"

function spark -d "sparkline generator"
    if isatty
        switch "$argv"
            case {,-}-v{ersion,}
                echo "spark version $spark_version"
            case {,-}-h{elp,}
                echo "usage: spark [--min=<n> --max=<n>] <numbers...>  Draw sparklines"
                echo "examples:"
                echo "       spark 1 2 3 4"
                echo "       seq 100 | sort -R | spark"
                echo "       awk \\\$0=length spark.fish | spark"
            case \*
                echo $argv | spark $argv
        end
        return
    end

    command awk -v FS="[[:space:],]*" -v argv="$argv" '
        BEGIN {
            min = match(argv, /--min=[0-9]+/) ? substr(argv, RSTART + 6, RLENGTH - 6) + 0 : ""
            max = match(argv, /--max=[0-9]+/) ? substr(argv, RSTART + 6, RLENGTH - 6) + 0 : ""
        }
        {
            for (i = j = 1; i <= NF; i++) {
                if ($i ~ /^--/) continue
                if ($i !~ /^-?[0-9]/) data[count + j++] = ""
                else {
                    v = data[count + j++] = int($i)
                    if (max == "" && min == "") max = min = v
                    if (max < v) max = v
                    if (min > v ) min = v
                }
            }
            count += j - 1
        }
        END {
            n = split(min == max && max ? "▅ ▅" : "▁ ▂ ▃ ▄ ▅ ▆ ▇ █", blocks, " ")
            scale = (scale = int(256 * (max - min) / (n - 1))) ? scale : 1
            for (i = 1; i <= count; i++)
                out = out (data[i] == "" ? " " : blocks[idx = int(256 * (data[i] - min) / scale) + 1])
            print out
        }
    '
end
### END OF SPARK ###


### Aliases ###
alias clear='echo -en "\x1b[2J\x1b[1;1H" ; echo;  seq 1 (tput cols) | sort -R | spark | lolcat' # Cute Spark animation on clear

alias ls='exa -l --color=always --group-directories-first' # my preferred listing
alias lt='exa -aT --color=always --group-directories-first' # tree listing

alias ..='cd ..'

end


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if test -f /home/main/miniforge3/bin/conda
    eval /home/main/miniforge3/bin/conda "shell.fish" "hook" $argv | source
end
# <<< conda initialize <<<

starship init fish | source
