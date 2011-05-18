function [state, options,optchanged] = gasave(options,state,flag,interval)

global disp_os;
global save_os;
global TgtFnc;

optchanged = false;

if (strcmp(flag,'done')), return; end
if (rem(state.Generation,100) ~= 0), return; end

if (save_os == 1)
    save gaautosave state
end

[fbest best] = min(state.Score);

% GD-in-the-loop
% if ((rem(state.Generation,2500)==0) && (state.Generation ~= 0))
%     [null worst] = max(state.Score);
%     
%     x0 = state.Population(best,:);
%     evalc('[x1 fv] = fminunc(TgtFnc,x0,optimset(''LargeScale'',''on'',''MaxFunEvals'',Inf,''MaxIter'',10));');
%     
%     state.Population(worst,:) = x1;
%     state.Score(worst) = fv;
%     
%     [fbest best] = min(state.Score);
% end

if (disp_os == 1)
    x = state.Population(best,:);

    if (state.Generation == 0)
        h = figure('Name','Optimal Stimuli','NumberTitle','off');
        set(h, 'Tag','gaplotbestindiv');
    else
        h = findobj('Tag','gaplotbestindiv');
        set(0,'CurrentFigure',h);
    end

    imagesc(reshape(x,[sqrt(numel(x)) sqrt(numel(x))])); colormap(gray);
else
    fprintf('GA Generation %d Fitness %f\n', state.Generation, fbest);
end