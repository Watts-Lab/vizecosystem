# local modules (parsers)
import parser_functions.main_grouped as main_grouped
import parser_functions.main_timeseries as main_timeseries
import parser_functions.main_timeseries_audiences as main_timeseries_audiences
import parser_functions.section_1 as section1
# import parser_functions.fig2 as fig2
# import parser_functions.fig3 as fig3
# import parser_functions.fig4 as fig4
# import parser_functions.fig5 as fig5
# import parser_functions.fig6 as fig6
# import parser_functions.fig7 as fig7
# import parser_functions.table2 as table2
# import parser_functions.video_count as video

class Parser:
  def __init__(self, creds):
    self.creds =  creds
    self.steps = {
      'EchoCh-by_state.csv': main_grouped.parse,
      'EchoCh-by_state_full-timeseries.csv': main_timeseries.parse,
      'EchoCh-TV-by_state_audiences.csv': main_timeseries_audiences.parse,
      'EchoCh-nationwide-by_gender-or-age_group.csv': section1.parse,
      # 'updated plots/all_7K/fig2A_ledwich.csv': fig2.parseA,
      # 'updated plots/all_7K/fig2B_ledwich.csv': fig2.parseB,
      # 'updated plots/all_7K/fig3A_ledwich.csv': fig3.parseA,
      # 'updated plots/all_7K/fig3B_ledwich.csv': fig3.parseB,
      # 'outdated plots/Fig4_transition_matrix.txt': fig4.parse,
      # 'outdated plots/Fig5.txt': fig5.parse,
      # 'outdated plots/Fig6_heatmap_matrix.txt': fig6.parse,
      # 'outdated plots/Fig7A_one_sessiontype_60_10.txt': fig7.parseA,
      # 'outdated plots/Fig7B_meanr.txt': fig7.parseB,
      # 'updated plots/all_7K/table2_ledwich.csv': table2.parse,
      # 'daily_collections/video_count.csv': video.parse
    }

  def parse(self, file):
    return self.steps[file["out_name"]](file)