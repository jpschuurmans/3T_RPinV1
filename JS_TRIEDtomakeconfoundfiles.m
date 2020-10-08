clear; clc;
outdir = '/home/jschuurmans/Documents/02_recurrentSF_3T/Data_BIDS/firstlevel';
D = dir(['/home/jschuurmans/Documents/02_recurrentSF_3T/Data_BIDS/fmriprep/sub-01/ses-*','/func/', '*mainExp_run', '*confounds_regressors.tsv']);
sub = 'sub-01';

%what confounds do I want to save? In the correct order:
columns = ["framewise_displacement", "trans_x", "trans_y","trans_z","rot_x","rot_y","rot_z"];

filenames = {D(:).name}.';
data = cell(length(D),1);


for ii = 1: length(D)
    %get file path
    fullname = [D(ii).folder '/' D(ii).name];

    skipCol = '%*s ';
    getCol = ' %s %*[^\n]';
    formatSpec = '%s';

    %read the data
    fid = fopen(fullname);
    %get information from file, such as headers.. 
    contain = textscan(fid, formatSpec,-Inf); headers = contain{1}; fclose(fid); 
    
    %preallocation-ish too lazy to do it properly
    confoundData = [];
        
    for jj = 1: length(columns)
        index = find(not(~contains(headers,columns(jj))));

        string = [repmat(skipCol,1,index(1)-1) getCol];
        fid = fopen(fullname);
        data = textscan(fid, string, 'headerLines', 1);
        fclose(fid);
        
        confoundData(:,jj) = str2double(data{1,1});
        
    end
    
    confoundData(isnan(confoundData)) = 0;
    
     
    %get runname and sessionname
    %because naming is a bit crappy this depends on if a run # is higher or
    %lower than 10 (numbers below 10 dont contain a 0 in naming)
    run = fullname(end-34:end-30);
    if ~contains(run, 'run')
        run = ['run-' run(end-1:end)];
        ses = fullname(end-55:end-50);
    elseif not(~contains(run, 'run'))
        run = ['run-0' run(end:end)];
        ses = fullname(end-54:end-49);
    end

    name = [outdir '/' sub '/' run '/' sub '_' ses '_' run '_confounds.tsv'];
    %writematrix(confoundData,name,'Delimiter','\t')
    dlmwrite(name,confoundData,'Delimiter','\t')
end

