clc
clear
close all


% Specify the path to the JSON file
% jsonFilePath = '../data/cyc03/MS01_soa_20231003_193347.json';
% jsonFilePath = '../data/cyc03/MS01_soa_20231004_114030.json';
jsonFilePath = '../data/cyc03/MS01_soa_20231004_150511.json';


% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);

% convert structure to arrays
soa_cell = struct2cell(jsonData.soa_cnd);
cue = struct2cell(jsonData.cued_image);
im1_x_cell = struct2cell(jsonData.im1_pos);
resp = struct2cell(jsonData.soa_response);
rt_cell =  struct2cell(jsonData.soa_rt);
cong_cell = struct2cell(jsonData.congruency);

nboot = 10000;

% modify cells
for i = 1:numel(soa_cell)
    if isempty(soa_cell{i})
        soa(i,1) = nan;
        im1_x(i,1) = nan;
        rt(i,1) = nan;
        cong(i,1) = nan;
    else
        soa(i,1) = soa_cell{i};
        im1_x(i,1) = im1_x_cell{i}(1);
        rt(i,1) = rt_cell{i};
        cong(i,1) = cong_cell{i};
    end
end

x = unique(soa);
x(isnan(x)) = [];
x_ms = x * 1000 / 60;

left_resp = strcmp(resp, 'l');

for isoa = 1:length(x)
    ind_att1 = (soa == x(isoa)) & (strcmp(cue, 'h') & (cong == 1));
    ind_att2 = (soa == x(isoa)) & (strcmp(cue, 'f') & (cong == 1));
    ind_att = ind_att1 | ind_att2;
    p_att(isoa) = sum(left_resp(ind_att)) / sum(ind_att) * 100;    
    rt_att(isoa) = mean(rt(ind_att));
    rt_att_err(isoa) = SE(rt(ind_att));
    for iboot = 1:nboot
        target_trials = find(ind_att);
        sample_trials = datasample(target_trials, length(target_trials));
        p_att_boot(iboot, isoa) = sum(left_resp(sample_trials)) / length(sample_trials) * 100;
    end

    ind_unatt1 = (soa == x(isoa)) & (strcmp(cue, 'f') & (cong == -1));
    ind_unatt2 = (soa == x(isoa)) & (strcmp(cue, 'h') & (cong == -1));
    ind_unatt = ind_unatt1 | ind_unatt2;
    p_unatt(isoa) = sum(left_resp(ind_unatt)) / sum(ind_unatt) * 100;    
    rt_unatt(isoa) = mean(rt(ind_unatt));
    rt_unatt_err(isoa) = SE(rt(ind_unatt));
    for iboot = 1:nboot
        target_trials = find(ind_unatt);
        sample_trials = datasample(target_trials, length(target_trials));
        p_unatt_boot(iboot, isoa) = sum(left_resp(sample_trials)) / length(sample_trials) * 100;
    end
end

figure('units','normalized','outerposition',[.2 .2 .3 .7])

% figure 1: bootstrapped accuracy

subplot(2,1,1)
hold on
hatt = errorbar(x_ms, median(p_att_boot), std(p_att_boot), 'or', 'linewidth', 1);
hunatt = errorbar(x_ms, median(p_unatt_boot), std(p_unatt_boot), 'ok', 'linewidth', 1);
yline(50)
xline(0)
legend Attended Unattended location northwest
cleanplot

ylim([-10 110])

xlabel 'Left image lead (ms)'
ylabel 'Reporting left image first (%)'

% figures 2: reaction time

x = unique(soa);
x(isnan(x)) = [];
x_ms = x * 1000 / 60;

subplot(2,1,2)
hold on
errorbar(x_ms, rt_att, rt_att_err, '-or', 'linewidth', 1);
errorbar(x_ms, rt_unatt, rt_unatt_err, '-ok', 'linewidth', 1);
cleanplot

xlabel 'Left image lead (ms)'
ylabel 'Reaction time (ms)'

rt_improvement = mean(-(rt_att-rt_unatt) ./ (rt_att+rt_unatt));
text(-50, 300, ['RT improvement: ', num2str(round(rt_improvement,1)),'%'])

%% Models
x_model = -250:250;
p_att = p_att';
p_unatt = p_unatt';

% Set up fittype and options.
ft = fittype( 'a/(1+exp(-k*(x-x0)))', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares');
opts.Display = 'Off';
opts.Lower = [-inf -inf -inf];
opts.Upper = [inf inf inf];
opts.StartPoint = [100 .1 0];

% Fit model to data.
[fitresult_att, gof_att] = fit(x_ms, p_att, ft, opts);
model_att = feval(fitresult_att, x_model);

[fitresult_unatt, gof_unatt] = fit(x_ms, p_unatt, ft, opts);
model_unatt = feval(fitresult_unatt, x_model);

subplot(2,1,1)
hold on
hattm = plot(x_model, model_att, 'r', 'linewidth', 1.5);
hunattm = plot(x_model, model_unatt, 'k', 'linewidth', 1.5);
legend([hatt hunatt hattm hunattm],...
    'Attended', 'Unattended', 'Model-att.', 'Model-unatt.', 'location', 'northwest');

adjr2_att = gof_att.adjrsquare
adjr2_unatt = gof_unatt.adjrsquare

k_att = fitresult_att.k
k_unatt = fitresult_unatt.k

att_improvement = (k_att-k_unatt)/(k_att + k_unatt);
text(50, 20, ['Accuracy improvement: ', num2str(round(att_improvement,1))])

%% Adjusted models

figure('units','normalized','outerposition',[.5 .5 .3 .4])
hold on
hatt = errorbar(x_ms-fitresult_att.x0, median(p_att_boot), std(p_att_boot), 'or', 'linewidth', 1);
hattm = plot(x_model-fitresult_att.x0, model_att, 'r', 'linewidth', 1.5);
hunatt = errorbar(x_ms-fitresult_unatt.x0, median(p_unatt_boot), std(p_unatt_boot), 'ok', 'linewidth', 1);
hunattm = plot(x_model-fitresult_unatt.x0, model_unatt, 'k', 'linewidth', 1.5);

xlim([-250, 250])
ylim([-10 110])

xlabel 'Left image lead (ms)'
ylabel 'Reporting left image first (%)'
xline(0)
yline(50)

legend([hatt hunatt hattm hunattm],...
    'Attended', 'Unattended', 'Model-att.', 'Model-unatt.', 'location', 'northwest');

cleanplot
