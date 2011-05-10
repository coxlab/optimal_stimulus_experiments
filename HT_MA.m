function output = HT_MA(input,network,c,Lmax)

Lmin = 1;
%Lmax = 2; %size(network, 2);

if (Lmax == 2)
    isize = 16;
elseif (Lmax == 3)
    isize = 46;
else
    isize = 106;
end

input = reshape(input, [isize isize]);

for l = Lmin:Lmax
    
    % Filter
    if (network{l}.filt.size ~= 0)
        if (l ~= Lmax)
            filt_size = size(input,1) - network{l}.filt.size + 1;
            filt = zeros(filt_size, filt_size, network{l}.filt.number);
        
            for f = 1:network{l}.filt.number
                filt(:,:,f) = convn(input, network{l}.filt.weights{f}, 'valid');
            end
        else
            filt = convn(input, network{l}.filt.weights{c}, 'valid');
        end
    else
        filt = input;
    end
    
    % Activate
    actv = filt;
    actv(actv(:) < network{l}.actv.min) = network{l}.actv.min;
    actv(actv(:) > network{l}.actv.max) = network{l}.actv.max;
    
    % Pool
    if (network{l}.pool.size ~= 0)
        pool = convn(actv .^ network{l}.pool.order, ones(network{l}.pool.size), 'valid') .^ (1 / network{l}.pool.order);
        pool = pool(1:network{l}.pool.stride:end, 1:network{l}.pool.stride:end, :);
    else
        pool = actv;
    end
    
    % Normalize
    if (l ~= Lmax)
        P_sum = convn(pool, ones(network{l}.norm.size, network{l}.norm.size, network{l}.filt.number), 'valid');
        P_ssum = convn(pool .^ 2, ones(network{l}.norm.size, network{l}.norm.size, network{l}.filt.number), 'valid');

        P_mean = P_sum / ((network{l}.norm.size ^ 2) * network{l}.filt.number);

        pos_min = (network{l}.norm.size + 1) / 2;
        pos_max = pos_min + size(pool,1) - network{l}.norm.size;

        if (network{l}.norm.centering == 1)
            C = pool(pos_min:pos_max, pos_min:pos_max, :) - repmat(P_mean, [1 1 network{l}.filt.number]);
            C_norm = P_ssum - (P_sum .^ 2)/((network{l}.norm.size ^ 2) * network{l}.filt.number);
            %C_norm(C_norm(:) < 0) = 0;
            C_norm = C_norm .^ 0.5;
        else
            C = pool(pos_min:pos_max, pos_min:pos_max, :);
            C_norm = P_ssum .^ 0.5;
        end

        %C_norm = C_norm + 1e-5;
        C_norm(C_norm(:) < (network{l}.norm.threshold/network{l}.norm.gain)) = 1/network{l}.norm.gain;
        norm = C ./ repmat(C_norm, [1 1 network{l}.filt.number]);
    else
        norm = pool;
    end
    
    % Next Layer or Output
    if (l ~= Lmax)
        input = norm;
    else
        output = -norm;
    end
    
    %figure; imagesc(norm(:,:,1));
    %figure; hist(norm(:));
end