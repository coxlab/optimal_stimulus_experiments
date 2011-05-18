function mutationChildren = limmutationgaussian(parents,options,GenomeLength,FitnessFcn,state,thisScore,thisPopulation,scale,shrink)

if(strcmpi(options.PopulationType,'doubleVector'))

    if nargin < 9 || isempty(shrink)
        shrink = 1;
        if nargin < 8 || isempty(scale)
            scale = 1;
        end
    end

    if (shrink > 1) || (shrink < 0)
        msg = sprintf('Shrink factors that are less than zero or greater than one may \n\t\t result in unexpected behavior.');
        warning('globaloptim:mutationgaussian:shrinkFactor',msg);
    end

    scale = scale - shrink * scale * state.Generation/options.Generations;

    range = options.PopInitRange;
    lower = range(1,:);
    upper = range(2,:);
    scale = scale * (upper - lower);

    mutationChildren = zeros(length(parents),GenomeLength);
    for i=1:length(parents)
        parent = thisPopulation(parents(i),:);
        mutationChildren(i,:) = parent  + scale .* randn(1,length(parent));
    end
    
    mutationChildren(mutationChildren(:) >  1) =  1;
    mutationChildren(mutationChildren(:) < 0) = 0;
else
    fprintf('GA Mutation Error!\n');
end
