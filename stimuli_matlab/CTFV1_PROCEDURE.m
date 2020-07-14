close all; clear all; clc
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/stimuli_matlab/'


% Procedure
blockdur=10000;
fixationDur=([10000]);
startend = 12000*2; % 2x also the end fix
checkerRuns = 2*10000
nblockspercondition=20; %% in total
% nchecker = 5; %% in total
totalnrun=20; % or 3
nblockperrun=24;

%this part is for dynamic noise steps
%gradcycle=6; % HZ
%framesperblock=blockdur/(1000/gradcycle);
%ntemplates=gradcycle;
%ngrad=framesperblock/ntemplates;
%gradsteps=linspace(0,1,ngrad+1); % +1 because the last step is dropped (redundant with the next step sequence)
%nsteps=length(gradsteps);

stimtype={'intact','negated','scrambled'};
masktype={'LSF','HSF'};


%frameDur=blockdur/framesperblock;
stimDur=([50,83,100,150]);

Cond1levels=(stimtype);
Cond2levels=stimDur;
Cond3levels=(masktype);
%image names should indicate the condition
nconditions=length(Cond1levels)*length(Cond2levels)*length(Cond3levels); % total number of conditions
ntotatlblock=(nblockspercondition*nconditions)%+nchecker; % in total
% ntotatlblock=(nblockspercondition*nconditions); % in total

runduration=((nblockperrun*(blockdur+fixationDur))+(startend)+(checkerRuns))/60000;
totalduration=runduration*totalnrun;

count=0;
condname={1:nconditions+1};
for level1=1:length(Cond1levels)
    for level2=1:length(Cond2levels)
        for level3=1:length(Cond3levels)
            count=count+1;
            temp=strcat(Cond1levels{level1},'_dur',num2str(Cond2levels(level2)),'_',strcat(Cond3levels{level3}));
            condname{count}=temp;
        end
    end
end

% condname{nconditions+1}='checker';


% bufferdur=4; % min amount of frames separating face occurrences
% Onset=bufferdur:3:(framesperblock-bufferdur); % we may want to vary this across blocks so that faces onset varies a bit over blocks
% nfaceperblk=length(Onset);
save([basefolder 'CTFV1_PROC.mat'])
