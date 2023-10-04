clc
clear
close all


% Specify the path to the JSON file
% jsonFilePath = '../data/cyc03/SC01_soa_20230929_120711.json';
% jsonFilePath = '../data/cyc03/AD01_soa_20231002_114655.json';
jsonFilePath = '../data/cyc03/MS01_soa_20231003_193347.json';


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
cong_cell = struct2cell(jsonData.congurency);

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

cue_ref = 'h';

for isoa = 1:length(x)
%     ind = (soa == x(isoa)) & (cong == 1);
    ind = (soa == x(isoa)) & (cong == 1) & (strcmp(cue, cue_ref));
    right_perc_cong(isoa) = sum(left_resp(ind)) / sum(ind) * 100;
    
    rt_cong(isoa) = mean(rt(ind));
    rt_err_cong(isoa) = SE(rt(ind));

    for iboot = 1:nboot
        target_trials = find(ind);
        sample_trials = datasample(target_trials, length(target_trials));
        right_perc_cong_boot(iboot, isoa) = sum(left_resp(sample_trials)) / length(sample_trials) * 100;
    end

%     ind = (soa == x(isoa)) & (cong == -1);
    ind = (soa == x(isoa)) & (cong == -1) & (strcmp(cue, cue_ref));
    right_perc_incong(isoa) = sum(left_resp(ind)) / sum(ind) * 100;

    rt_incong(isoa) = mean(rt(ind));
    rt_err_incong(isoa) = SE(rt(ind));

    for iboot = 1:nboot
        target_trials = find(ind);
        sample_trials = datasample(target_trials, length(target_trials));
        right_perc_incong_boot(iboot, isoa) = sum(left_resp(sample_trials)) / length(sample_trials) * 100;
    end
end

figure('units','normalized','outerposition',[.3 2 .3 .7])

% figure 1: bootstrapped accuracy

subplot(2,1,1)
hold on
hcong = errorbar(x_ms, median(right_perc_cong_boot), std(right_perc_cong_boot),...
    '-ok');
hincong = errorbar(x_ms, median(right_perc_incong_boot), std(right_perc_incong_boot),...
    '-or');
yline(50)
xline(0)
legend cong incong location northwest
cleanplot

xlabel 'Left image lead (ms)'
ylabel 'Reporting left image first (%)'

% figures 2: reaction time

x = unique(soa);
x(isnan(x)) = [];
x_ms = x * 1000 / 60;

subplot(2,1,2)
hold on
errorbar(x_ms, rt_cong, rt_err_cong, '-ok', 'linewidth', 1);
errorbar(x_ms, rt_incong, rt_err_incong, '-or', 'linewidth', 1);
cleanplot

xlabel 'Left image lead (ms)'
ylabel 'Reaction time (ms)'

%% Models
y_cong = right_perc_cong';
y_incong = right_perc_incong';
x_model = -250:250;
% x_ms = [x_ms(1:3)'-100 x_ms' x_ms(end-2:end)'+100]';
% y_cong = [0 0 0 right_perc_cong 100 100 100]';
% y_incong = [0 0 0 right_perc_incong 100 100 100]';

% [x_ms, yData] = prepareCurveData(x_ms, y_cong);

% Set up fittype and options.
ft = fittype( 'a/(1+exp(-k*(x-x0)))', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares');
opts.Display = 'Off';
opts.Lower = [-Inf 0 -150];
opts.Upper = [Inf 1 150];
opts.StartPoint = [100 .5 0];

% Fit model to data.
[fitresult_cong, gof_cong] = fit(x_ms, y_cong, ft, opts);
model_cong = feval(fitresult_cong, x_model);

[fitresult_incong, gof_incong] = fit(x_ms, y_incong, ft, opts);
model_incong = feval(fitresult_incong, x_model);

subplot(2,1,1)
hold on
hcongm = plot(x_model, model_cong, '--k', 'linewidth', 1.5);
hincongm = plot(x_model, model_incong, '--r', 'linewidth', 1.5);

legend([hcong hincong hcongm hincongm],...
    'cong', 'incong', 'cong-model', 'incong-model', 'location', 'northwest');

adjr2_cong = gof_cong.adjrsquare
adjr2_incong = gof_incong.adjrsquare

%% Adjusted models

figure
hold on
hcong = plot(x_ms-fitresult_cong.x0, y_cong, 'ok', 'linewidth', 1);
hcongm = plot(x_model-fitresult_cong.x0, model_cong, 'k', 'linewidth', 1.5);
hincong = plot(x_ms-fitresult_incong.x0, y_incong, 'or', 'linewidth', 1);
hincongm = plot(x_model-fitresult_incong.x0, model_incong, 'r', 'linewidth', 1.5);

xlim([-250, 250])
ylim([-10 110])

xlabel 'Left image lead (ms)'
ylabel 'Reporting left image first (%)'
xline(0)
yline(50)

legend([hcong hincong hcongm hincongm],...
    'cong', 'incong', 'cong-model', 'incong-model', 'location', 'northwest');

cleanplot

k_cong = fitresult_cong.k
k_incong = fitresult_incong.k

