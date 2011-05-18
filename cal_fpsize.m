function footprint = cal_fpsize(network,Lmax,observ)

footprint = 1;

if (nargin == 2), observ = 'pool'; end

for l = Lmax:-1:1
    % Normalize
    if (network{l}.norm.size ~= 0)
        if ((l~=Lmax) || strcmp(observ,'norm'))
            footprint = footprint + network{l}.norm.size - 1;
        end
    end
    
    % Pool
    if (network{l}.pool.size ~= 0)
        footprint = (footprint-1)*network{l}.pool.stride + network{l}.pool.size;
    end
    
    % Filter
    if (network{l}.filt.size ~= 0)
        footprint = footprint + network{l}.filt.size - 1;
    end
end