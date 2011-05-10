layer = 1;

filt.size = 0; filt.number = 1;
actv.min = -Inf; actv.max = Inf; 
pool.size = 0; pool.order = 0; pool.stride = 0;
norm.size = 9; norm.centering = 0; norm.gain = 1.0; norm.threshold = 1.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 2;

filt.size = 3; filt.number = 16;
actv.min = 0; actv.max = Inf; 
pool.size = 5; pool.order = 2; pool.stride = 2;
norm.size = 9; norm.centering = 0; norm.gain = 0.1; norm.threshold = 10.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 3;

filt.size = 3; filt.number = 32;
actv.min = 0; actv.max = Inf; 
pool.size = 5; pool.order = 10; pool.stride = 2;
norm.size = 5; norm.centering = 1; norm.gain = 0.1; norm.threshold = 10.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

layer = 4;

filt.size = 3; filt.number = 128;
actv.min = -Inf; actv.max = 1; 
pool.size = 9; pool.order = 2; pool.stride = 2;
norm.size = 3; norm.centering = 0; norm.gain = 0.1; norm.threshold = 1.0;

network{layer}.filt = filt;
network{layer}.actv = actv;
network{layer}.pool = pool;
network{layer}.norm = norm;

clear layer filt actv pool norm;

TW = 0;
TZ = 0;
sparsity = 0.0;
bias = 1;

for i = 1:4
    if (network{i}.filt.size ~= 0)
        network{i}.filt.weights = cell(1,network{i}.filt.number);
        for j = 1:network{i}.filt.number
            network{i}.filt.weights{j} = rand(network{i}.filt.size, network{i}.filt.size, network{i-1}.filt.number);
            % network{i}.filt.weights{j} = randn(network{i}.filt.size, network{i}.filt.size, network{i-1}.filt.number);
            
            % Location Sparse
            sparse_idx = false(numel(network{i}.filt.weights{j}), 1);
            sparse_idx(1:floor(sparsity*numel(network{i}.filt.weights{j}))-bias, 1) = true;
            sparse_idx = sparse_idx(randperm(numel(network{i}.filt.weights{j})), 1);
            network{i}.filt.weights{j}(~sparse_idx) = network{i}.filt.weights{j}(~sparse_idx) - mean(network{i}.filt.weights{j}(~sparse_idx));
            
            % Value Sparse
            % network{i}.filt.weights{j} = network{i}.filt.weights{j} - mean(network{i}.filt.weights{j}(:));
            % sparse_idx = abs(network{i}.filt.weights{j}(:)) < sparsity*max(abs(network{i}.filt.weights{j}(:)));
            
            TW = TW + numel(network{i}.filt.weights{j});
            TZ = TZ + length(find(sparse_idx));
            
            network{i}.filt.weights{j}(sparse_idx) = 0;
            network{i}.filt.weights{j} = network{i}.filt.weights{j} / norm(network{i}.filt.weights{j}(:));
            
            %network{i}.filt.weights{j} = single(network{i}.filt.weights{j});
        end
    end
end

fprintf('Overall Filter Sparsity: %f\n', TZ / TW);
clear i j sparsity sparse_idx TW TZ bias;
