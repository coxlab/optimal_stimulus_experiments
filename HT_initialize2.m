layer = 1;

filt.size = 0; filt.number = 1;
actv.min = -Inf; actv.max = Inf; 
pool.size = 0; pool.order = 0; pool.stride = 0;
norm.size = 3; norm.centering = 0; norm.gain = 1.0; norm.threshold = 0.1;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 2;

filt.size = 7; filt.number = 32;
actv.min = 0; actv.max = 1; 
pool.size = 9; pool.order = 1; pool.stride = 2;
norm.size = 3; norm.centering = 0; norm.gain = 0.1; norm.threshold = 1.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 3;

filt.size = 5; filt.number = 128;
actv.min = 0; actv.max = 1; 
pool.size = 7; pool.order = 2; pool.stride = 2;
norm.size = 5; norm.centering = 1; norm.gain = 0.1; norm.threshold = 1.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 4;

filt.size = 5; filt.number = 128;
actv.min = -Inf; actv.max = Inf; 
pool.size = 9; pool.order = 10; pool.stride = 2;
norm.size = 7; norm.centering = 1; norm.gain = 0.1; norm.threshold = 1.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

clear layer filt actv pool norm;
RandStream.setDefaultStream(RandStream('mt19937ar','seed',0));

for i = 1:4
    if (network{i}.filt.size ~= 0)
        network{i}.filt.weights = cell(1,network{i}.filt.number);
        for j = 1:network{i}.filt.number
            network{i}.filt.weights{j} = rand(network{i}.filt.size, network{i}.filt.size, network{i-1}.filt.number);
            network{i}.filt.weights{j} = network{i}.filt.weights{j} - mean(network{i}.filt.weights{j}(:));
            network{i}.filt.weights{j} = network{i}.filt.weights{j} / norm(network{i}.filt.weights{j}(:));
            %network{i}.filt.weights{j} = randn(network{i}.filt.size, network{i}.filt.size, network{i-1}.filt.number);
        end
    end
end

clear i j;
RandStream.setDefaultStream(RandStream('mt19937ar','seed',sum(100*clock)));