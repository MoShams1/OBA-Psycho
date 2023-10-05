clc
clear
close all


% Specify the path to the JSON file
jsonFilePath = '../data/cyc03/MS01_task2_soa_20231004_181052.json';

% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);

% convert structure to arrays
soa_cell = struct2cell(jsonData.soa_cnd);
cue = struct2cell(jsonData.cued_image);
im1_cat = struct2cell(jsonData.im1_category);
resp_eval = cell2mat(struct2cell(jsonData.soa_resp_eval));
rt_cell =  struct2cell(jsonData.soa_rt);

nboot = 10000;

% modify cells
for i = 1:numel(soa_cell)
    if isempty(soa_cell{i})
        soa(i,1) = nan;
        rt(i,1) = nan;
    else
        soa(i,1) = soa_cell{i};        
        rt(i,1) = rt_cell{i};
    end
end

obj = 'h';
other_obj = setdiff(['f','h'],obj);

% ind_att = strcmp(im1_cat, obj) & (soa>0) & (strcmp(cue, obj));
ind_att = strcmp(cue, obj);
p_att = sum(resp_eval(ind_att)) / sum(ind_att) * 100;    
rt_att = mean(rt(ind_att));
rt_att_err = SE(rt(ind_att));
for iboot = 1:nboot
    target_trials = find(ind_att);
    sample_trials = datasample(target_trials, length(target_trials));
    p_att_boot(iboot,1) = sum(resp_eval(sample_trials)) / length(sample_trials) * 100;
end

% ind_unatt = strcmp(im1_cat, obj) & (soa>0) & (strcmp(cue, other_obj));
ind_unatt = strcmp(cue, other_obj);
p_unatt = sum(resp_eval(ind_unatt)) / sum(ind_unatt) * 100;    
rt_unatt = mean(rt(ind_unatt));
rt_unatt_err = SE(rt(ind_unatt));
for iboot = 1:nboot
    target_trials = find(ind_unatt);
    sample_trials = datasample(target_trials, length(target_trials));
    p_unatt_boot(iboot,1) = sum(resp_eval(sample_trials)) / length(sample_trials) * 100;
end

figure('units','normalized','outerposition',[.2 .2 .2 .7])

subplot(2,1,1)
errorbar([1,2],...
    [mean(p_unatt_boot), mean(p_att_boot)],...
    [std(p_unatt_boot), std(p_att_boot)], '-ok')
xticks([1 2])
xticklabels({'Unatt.', 'Att.'})
xlim([.5 2.5])
ylim([30 70])
yline(50)
ylabel 'Response accuracy (%)'
cleanplot

subplot(2,1,2)
errorbar([1,2],...
    [rt_unatt, rt_att],...
    [rt_unatt_err, rt_att_err], '-ok')
xticks([1 2])
xticklabels({'Unatt.', 'Att.'})
xlim([.5 2.5])
ylabel 'RT (ms)'
cleanplot
