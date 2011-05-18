function Run_MA(network,Lmax,Ch,gennum,psize)

resume = 0;
constrained = 0;
useparallel = 0;
flatinit = 0;

global disp_os; disp_os = 1;
global save_os; save_os = 0;
global gd_log_freq; gd_log_freq = 10;
global TgtFnc;

if (nargin <= 3), gennum = 5000; end
if (nargin <= 4), psize = 32; end

if (resume == 0) % New Start
    isize = cal_fpsize(network,Lmax,'pool');
    
    if (isempty(Ch)), Ch = 1:network{Lmax}.filt.number; end
    SCh = 1;

    if (flatinit == 1)
        population = zeros(psize, isize*isize); scores = [];
    else
        population = []; scores = [];
    end
    
    if (constrained == 0)
        fmut = @mutationgaussian;
        fmin = @fminunc;
        Cmin = [];
        Cmax = [];
        Vmin = -0.5; Vmax = 0.5;
    else
        fmut = @limmutationgaussian;
        fmin = @fmincon;
        Cmin = ones(1,isize^2) * Vmin;
        Cmax = ones(1,isize^2) * Vmax;
        Vmin = 0; Vmax = 1;
    end
else
    % Load MAT
end

if (useparallel == 1)
    useparallelopt = 'always';
else
    useparallelopt = 'never';
end 

if (disp_os == 1)
    disp_ga = @gaplotbestf;
    disp_gd = {@optimplotfval @optimplotfirstorderopt};
else
    disp_ga = [];
    disp_gd = [];
end

options = gaoptimset('PopulationSize',psize,...
                     'PopInitRange',[Vmin;Vmax],...
                     'InitialPopulation',population,...
                     'InitialScores',scores,...
                     'EliteCount',psize/8,...
                     'Generations',gennum,...
                     'StallGenLimit',Inf,...
                     'TolFun',0,...
                     'CrossoverFcn',@crossoverintermediate,...
                     'MutationFcn',{fmut 1.0 0.0},...
                     'OutputFcns',@gasave,...
                     'HybridFcn',{fmin,optimset('PlotFcns',disp_gd,...
                                                'LargeScale','on',...
                                                'MaxFunEvals',Inf,...
                                                'MaxIter',Inf,...
                                                'OutputFcn',@gahybsave)},...
                     'UseParallel',useparallelopt,...
                     'PlotFcns',disp_ga);

for s = SCh
    for c = Ch
        TgtFnc = @(x)HT_MA(x,isize,network,c,Lmax,s);
        
        [x,f,exitFlag,output,population,scores] = ...
        ga(TgtFnc,isize*isize,[],[],[],[],Cmin,Cmax,[],options); 
        save(['MA_L' num2str(Lmax-1) '_C' num2str(c) '.mat']);
        
        xp = (x - min(x)) / (max(x) - min(x)); 
        xp = reshape(xp,[isize isize]);
        imwrite(imresize(xp,8,'method','nearest'), ['os_L' num2str(Lmax-1) '_c' num2str(c) '.png']);
    end
end