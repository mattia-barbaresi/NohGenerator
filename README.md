# NohGenerator & IT metrics

## required packages

    matplotlib
    deap
    numpy
    pyjarowinkler
    distance
    bcolors

## main directories

- ##### data
    moves archive, repertoires and results
    
- ##### evaluation
    Evaluation and IT metrics
    
- ##### genetic_algorithm
    directory of the GA implementation, using DEAP

- ##### nao_control
    Code for sending moves to the robot. It uses naoqi + CoppeliaSim robot simulator (simulated Nao)

- ##### nao_libs
    Contains library for converting mocap data joint angles into a json format for Nao

- ##### utils
    Lib for plotting results and maths
