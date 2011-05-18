function stop = gahybsave(x,optimValues,state,varargin)

global disp_os;
global save_os;
global gd_log_freq;

stop = false;

if (rem(optimValues.iteration,gd_log_freq) ~=0), return; end

if (save_os == 1)
    save gahybautosave x
end

if (disp_os == 1)
    h = findobj('Tag','gaplotbestindiv');
    set(0,'CurrentFigure',h);

    imagesc(reshape(x,[sqrt(numel(x)) sqrt(numel(x))])); colormap(gray);
else
    fprintf('GD Iteration %d Fitness %f\n', optimValues.iteration, optimValues.fval);
end