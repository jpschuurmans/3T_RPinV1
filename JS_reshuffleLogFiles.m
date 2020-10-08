clear; clc;
outdir = '/home/jschuurmans/Documents/02_recurrentSF_3T/Data_BIDS';
D = dir(['/home/jschuurmans/Documents/02_recurrentSF_3T/Data_raw/IG_PILOT_ses3_behav', '/*.csv']);
filenames = {D(:).name}.';
data = cell(length(D),1);
for ii = 1: length(D)
    %get file path
    fullname = [D(ii).folder '/' D(ii).name];
    %read the data
    fid = fopen(fullname);
    A = textscan(fid, '%s',  'Delimiter', '\n' );
    %select the correct rows
    B = A{1,1}(3:end-2); 
    fclose(fid);
    
    %split into columns (based on csv)
    C = cellfun(@(x)regexp(x,',','split'),B,'UniformOutput',0);
    
    %create a file with the correct headers
    %[onset	duration	trial_type	stim_file]
    X = ["onset", "duration", "trial_type", "stim_file"];
    
    for jj = 1: length(B)
        %get correct row
        E = C{jj}; 
        
        if jj == 604
            %take onset info (column F = 6)
            onset = E(6);
            %take duration info (column G = 7)
            duration = E(7);
        else
            %take onset info (column G = 7)
            onset = E(7);
            %take duration info (column H = 8)
            duration = E(8);
        end
        
        %make sure only int is taken (no string)
        onset = regexp(onset, '[\d*\.]*\d','match');
        onset = [onset{:}];
        onset=str2double(strcat(onset{:}));
        %set this onset value to the correct column in new file
        X(jj+1,1) = onset;
        
        %make sure only int is taken (no string)
        duration = regexp(duration, '[\d*\.]*\d','match');
        duration = [duration{:}];
        duration=str2double(strcat(duration{:}));
        %set this duration value to the correct column in new file
        X(jj+1,2) = duration;
        
        %take trial_type info (column E anf F = 5 and 6)
        trial = E(5);
        type = E(6);
        
        if any(strcmp(trial{1},'fixation'))
            trial_type = strcat(trial{:});
        elseif any(strcmp(trial{1},'None'))
            trial_type = 'n/a';
        else
            trial_type = [strcat(trial{:}) '_' strcat(type{:})];
        end
        
        %set this trial_type value to the correct column in new file
        X(jj+1,3) = trial_type;
        
        %take stim_file info (column L = 12)
        stim_file = E(12);
        
        
        if any(strcmp(stim_file{1},'None'))
            stim_file = 'n/a';
        else
            stim_file = strcat(stim_file{:});
        end
        %set this stim_file value to the correct column in new file
        X(jj+1,4) = stim_file;
        
        
    end

    %save this new file as tsv file
    
%     if ii < 6
%         ses = '02';
%     else
%         ses = '03';
%     end
    
%     if ii <10
%         name = [outdir '/sub-01_ses-' ses '_task-mainExp_run-0' num2str(ii) '_events.txt'];
%     else
%         name = [outdir '/sub-01_ses-' ses '_task-mainExp_run-' num2str(ii) '_events.txt'];
%         
%     end
    run = ii+12;
    name = [outdir '/sub-01_ses-04_task-mainExp_run-' num2str(run) '_events.txt'];
    

    writematrix(X,name,'Delimiter','\t') 
    
end

