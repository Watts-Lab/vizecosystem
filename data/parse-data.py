# # modules
from os import getenv
  
# # local modules
from parsers import Parser

# # global vars
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
BUCKET = getenv('BUCKET')

# # datasets
datasets = [
  {
    'url': [
      # # # tv
      'raw_data/all_adults_national_tv_consumption_f1.csv',
      'raw_data/by_age_national_tv_consumption_f1.csv',
      'raw_data/by_age_x_gender_national_tv_consumption_f1.csv',
      'raw_data/by_gender_national_tv_consumption_f1.csv',
      'raw_data/by_race_national_tv_consumption_f1.csv',
      'raw_data/by_gender_x_race_national_tv_consumption_f1.csv',
      'raw_data/by_age_x_race_national_tv_consumption_f1.csv',
      'raw_data/by_state_national_tv_consumption_f1.csv',
      # # # web
      'raw_data/all_adults_desktop_web_consumption_f1.csv',
      'raw_data/by_gender_desktop_web_consumption_f1.csv',
      'raw_data/by_age_desktop_web_consumption_f1.csv',
      'raw_data/by_age_x_gender_desktop_web_consumption_f1.csv',
      'raw_data/by_race_desktop_web_consumption_f1.csv',
      'raw_data/by_gender_x_race_desktop_web_consumption_f1.csv',
      'raw_data/by_age_x_race_desktop_web_consumption_f1.csv',
      'raw_data/by_state_desktop_web_consumption_f1.csv',
      # # # mobile
      'raw_data/PHN_all_adults_mobile_consumption_f1.csv',
      'raw_data/PHN_by_age_group_mobile_consumption_f1.csv',
      'raw_data/PHN_by_gender_mobile_consumption_f1.csv',
      'raw_data/PHN_by_race_mobile_consumption_f1.csv',
      'raw_data/PHN_by_gender_by_race_mobile_consumption_f1.csv',
      'raw_data/PHN_by_gender_by_age_group_mobile_consumption_f1.csv',
      'raw_data/PHN_by_age_group_by_race_mobile_consumption_f1.csv',
      'raw_data/PHN_by_state_mobile_consumption_f1.csv',
      # # # tables
      'raw_data/TAB_all_adults_mobile_consumption_f1.csv',
      'raw_data/TAB_by_age_group_mobile_consumption_f1.csv',
      'raw_data/TAB_by_gender_mobile_consumption_f1.csv',
      'raw_data/TAB_by_race_mobile_consumption_f1.csv',
      'raw_data/TAB_by_gender_by_race_mobile_consumption_f1.csv',
      'raw_data/TAB_by_gender_by_age_group_mobile_consumption_f1.csv',
      'raw_data/TAB_by_age_group_by_race_mobile_consumption_f1.csv',
      'raw_data/TAB_by_state_mobile_consumption_f1.csv',
    ],
    'out_name': 'EchoCh-national_consumption_tv_and_web.csv',
    'format': '%.3f'
  },
  {
    'url': [
      'raw_data/TVLeftEchoChLenient_by_state.csv',
      'raw_data/TVLeftEchoChStringent_by_state.csv',
      'raw_data/TVRightEchoChLenient_by_state.csv',
      'raw_data/web_ec_sizes_by_state.csv',
      ], 
    'out_name': 'EchoCh-by_state.csv',
    'format': '%.4f'
  },
  {
    'url': [
      'raw_data/TVLeftEchoChLenient_by_state.csv',
      'raw_data/TVLeftEchoChStringent_by_state.csv',
      'raw_data/TVRightEchoChLenient_by_state.csv',
      'raw_data/web_ec_sizes_by_state.csv',
      ], 
    'out_name': 'EchoCh-by_state_full-timeseries.csv',
    'format': '%.3f'
  },
  {
    'url': [
      'raw_data/tv_top_content_by_state_last_3_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_6_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_12_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_since_2016_top_programs.csv',
      'raw_data/desktop_top_content_by_state_last_3_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_6_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_12_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_since_2016_top_domains.csv',
    ],
    'out_name': 'EchoCh-by_state_audiences.csv',
    'format': '%.0f'
  },
  {
    'url': [
      'raw_data/tv_top_content_by_state_last_3_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_6_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_12_months_top_programs.csv',
      'raw_data/tv_top_content_by_state_last_since_2016_top_programs.csv',
      'raw_data/desktop_top_content_by_state_last_3_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_6_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_12_months_top_domains.csv',
      'raw_data/desktop_top_content_by_state_last_since_2016_top_domains.csv',
    ],
    'out_name': 'EchoCh-by_state_audiences_hyperpartisan.csv',
    'format': '%.0f'
  },
  {
    'url': [
      # # # TV L Lenient
      'raw_data/TVLeftEchoChLenient_all_adults.csv',
      'raw_data/TVLeftEchoChLenient_by_age_x_gender.csv',
      'raw_data/TVLeftEchoChLenient_by_age_x_race.csv',
      'raw_data/TVLeftEchoChLenient_by_age.csv',
      'raw_data/TVLeftEchoChLenient_by_gender_x_race.csv',
      'raw_data/TVLeftEchoChLenient_by_gender.csv',
      'raw_data/TVLeftEchoChLenient_by_race.csv',
      # # # TV L Stringent
      'raw_data/TVLeftEchoChStringent_all_adults.csv',
      'raw_data/TVLeftEchoChStringent_by_age_x_gender.csv',
      'raw_data/TVLeftEchoChStringent_by_age_x_race.csv',
      'raw_data/TVLeftEchoChStringent_by_age.csv',
      'raw_data/TVLeftEchoChStringent_by_gender_x_race.csv',
      'raw_data/TVLeftEchoChStringent_by_gender.csv',
      'raw_data/TVLeftEchoChStringent_by_race.csv',
      # # # TV R
      'raw_data/TVRightEchoChLenient_all_adults.csv',
      'raw_data/TVRightEchoChLenient_by_age_x_gender.csv',
      'raw_data/TVRightEchoChLenient_by_age_x_race.csv',
      'raw_data/TVRightEchoChLenient_by_age.csv',
      'raw_data/TVRightEchoChLenient_by_gender_x_race.csv',
      'raw_data/TVRightEchoChLenient_by_gender.csv',
      'raw_data/TVRightEchoChLenient_by_race.csv',
      # # # Web
      'raw_data/web_ec_sizes_all_adults.csv',
      'raw_data/web_ec_sizes_by_age_x_gender.csv',
      'raw_data/web_ec_sizes_by_age_x_race.csv',
      'raw_data/web_ec_sizes_by_age.csv',
      'raw_data/web_ec_sizes_by_gender_x_race.csv',
      'raw_data/web_ec_sizes_by_gender.csv',
      'raw_data/web_ec_sizes_by_race.csv',
    ], 
    'out_name': 'EchoCh-nationwide-by_gender-age-race.csv',
    'format': '%.3f'
  },
  {
    'url': 'raw_data/tv_archetype_flow_data_agg_networks=True.csv',
    'out_name': 'EchoCh-links.csv',
    'format': '%.3f'
  },
  {
    'url': [
      'raw_data/tv_archetype_sizes_agg_networks=True.csv',
      'raw_data/tv_archetype_mins_p_person_agg_networks=True.csv'
    ],
    'out_name': 'EchoCh-nodes.csv',
    'format': '%.5f'
  },
  {
    'url': 'raw_data/tv_archetype_net_change_in_size_agg_networks=True.csv',
    'out_name': 'EchoCh-nodes-net_change_in_size.csv',
    'format': '%.0f'
  },
]
# # credentials
creds = {
  "key": AWS_ACCESS_KEY_ID,
  "secret": AWS_SECRET_ACCESS_KEY
}
# # instantiate parser
file_parser = Parser(creds)

# # iterate over files that need parsing 
for file in datasets:
  out_data = file_parser.parse(file)

  # # save data to different location
  out_data.to_csv(
    f's3://{BUCKET}/processed/{file["out_name"]}',
    index=False,
    float_format=file["format"]
  )
