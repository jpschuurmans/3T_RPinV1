clear; clc;
outdir = '/home/jschuurmans/Documents/02_recurrentSF_3T/Data_BIDS/firstlevel';
D = dir(['/home/jschuurmans/Documents/02_recurrentSF_3T/Data_BIDS/sub-01/ses-*','/func/', '*mainExp','*.tsv']);
filenames = {D(:).name}.';
data = cell(length(D),1);
trialNum = 24 ; %nr of trials within one block
sub = 'sub-01';

for ii = 1: length(D)
    %get file path
    fullname = [D(ii).folder '/' D(ii).name];
    run = fullname(end-16:end-11);
    %read the data
    fid = fopen(fullname);
    A = textscan(fid, '%s %s %s %s',  'Delimiter', '\t' );
    fclose(fid);
    
    %fixationtrials
    typeFix = A{1,3}{2};
    fprintf('Fixation: %s\n', typeFix)
    fixInd = find(contains(A{1,3},typeFix));
    fixdur = ones(length(fixInd),3);
    
    for jj = 1:length(fixInd)
        fixdur(jj,1) = str2double(A{1,1}{fixInd(jj)});
        fixdur(jj,2) = str2double(A{1,2}{fixInd(jj)})/1000;
        
        if jj < length(fixInd)-1
            X = ones(1,3);
            fixIndex = fixInd(jj);
            vector = fixIndex+1:24+fixIndex;
        
            %get the onset of the block
            onset = A{1,1}; onset = onset(vector); %onsets
            onset = str2double(onset{1,1});
            X(1) = onset;
            
            %get the duration of block
            duration = A{1,2}; duration = duration(vector);%durations
            for hh = 1:length(duration)
                duration{hh,1} = str2double(duration{hh,1});
            end
            duration = sum(cell2mat(duration));
            X(2) = duration/1000;
            
            %get stimulus type
            stimtype = A{1,3}; stimtype = stimtype(vector);
            [s,~,j]=unique(stimtype); stimtype = s{mode(j)};
        
            %saving event files for conditions 
            name = [outdir '/' sub '/' run '/EV_' run  '_' stimtype '.txt'];
            writematrix(X,name,'Delimiter','\t') 

        end
        %saving event files  for fixation   
        name = [outdir '/' sub '/' run '/EV_' run  '_' typeFix '.txt'];
        writematrix(fixdur,name,'Delimiter','\t')
        
    end
    
    %checkerboards
    checker = A{1,3}{end-2};
    fprintf('Checkerboard: %s\n', typeFix)
    checkerInd = find(contains(A{1,3},checker));
    checkerdur = ones(length(checkerInd),3);
    for jj = 1:length(checkerInd)
        checkerdur(jj,1) = str2double(A{1,1}{checkerInd(jj)});
        checkerdur(jj,2) = str2double(A{1,2}{checkerInd(jj)})/1000;
    end
    Y = checkerdur(1,:);
    type = checker(1:end-4);
    name = [outdir '/' sub '/' run '/EV_' run  '_' type 'face.txt'];
    writematrix(Y,name,'Delimiter','\t')
    Y = checkerdur(2,:);
    type = checker(1:end-4);
    name = [outdir '/' sub '/' run '/EV_' run  '_' type 'back.txt'];
    writematrix(Y,name,'Delimiter','\t')

end