function [state, options,optchanged] = gasave(options,state,flag,interval)

optchanged = false;

if nargin <4
    interval = 100;
end
if interval <= 0
    interval = 100;
end

if (rem(state.Generation,interval) ~=0)
    return;
end

save gaautosave state

[fval,best] = min(state.Score);
x = state.Population(best,:);

if (state.Generation == 0)
    h = figure;
    set(h, 'Tag','gaplotbestindiv');
else
    h = findobj('Tag','gaplotbestindiv');
    set(0,'CurrentFigure',h);
end

imagesc(reshape(x,[sqrt(numel(x)) sqrt(numel(x))])); colormap(gray);

