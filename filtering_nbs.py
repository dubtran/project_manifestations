def filtering_data(d_arts, media): 
    art_sc = dict()
    for x in d_arts.keys():
        try:
            if media in d_arts[x].keys():
                 art_sc[x] = d_arts[x][media]
        except Exception, e:
            print e[0]
    return art_sc

def dateparser(datestring):
    return datetime.strptime(datestring,'%Y%m%d%H')

#finding movement over days 
def get_logmovement(artists):
    entire_difs = pd.DataFrame()

    for key, value in artists.iteritems():
        logged = pd.DataFrame(value)
        logged['plays'] = log(value['plays'])
        logged = logged.set_index('date')
        log_dif = logged.diff()
#         rr = log_dif.resample("W", how='mean')
#         _diff = move-rr
#         log_dif[key+'_reDif'] = _diff
        entire_difs = pd.concat([entire_difs,log_dif], axis = 1)
        entire_difs = entire_difs.rename(columns = {'plays': key})
    return entire_difs

def get_absMovement(artists):
    entire_df = pd.DataFrame()
    for a, val in artists.iteritems():
        temp = pd.DataFrame(val)
        temp['plays'] = log(abs(temp['plays'].diff()))
        entire_df = pd.concat([entire_df, temp], axis = 1)
        entire_df = entire_df.rename(columns = {'plays': a})
    return entire_df

def SC_df_helper(metric, m_name):
    
    play_df = pd.DataFrame.from_dict(metric)
    play_df.columns = ['date', m_name]
    play_df['date'] = pd.to_datetime(play_df['date'])
    play_df = play_df.sort('date').reset_index()
    play_df.pop('index')
    

    return play_df


def SCcreating_dfs(art_sc):
    dfs_plays = {}
    dfs_downloads = {}
    dfs_comments = {}
    dfs_fans = {}
    dfs_soundcloud = {}
    for x in art_sc.keys():

        if art_sc[x]['plays']:
            dfs_plays[ x.encode('ascii', errors = 'ignore').rstrip()] = SC_df_helper(art_sc[x]['plays'], 'plays') 

        if art_sc[x]['downloads']: 
            dfs_downloads[ x.encode('ascii', errors = 'ignore').rstrip()] = SC_df_helper(art_sc[x]['downloads'], 'downloads')

        if art_sc[x]['comments']:
            dfs_comments[x.encode('ascii', errors = 'ignore').rstrip()] = SC_df_helper(art_sc[x]['comments'], 'comments')

        if art_sc[x]['fans']:
            dfs_fans[x.encode('ascii', errors = 'ignore').rstrip()] = SC_df_helper(art_sc[x]['fans'], 'fans')

        full_df = pd.concat([play_df, download_df, comment_df, fan_df], axis = 1)
        dfs_soundcloud[x.encode('ascii', errors = 'ignore')] = full_df
    return dfs_plays, dfs_downloads, dfs_comments, dfs_fans, dfs_soundcloud

if if __name__ == '__main__':
    engine = create_engine('postgresql://dubT:!@localhost:5432/nebulae')
    Cnbs_data = pickle.load(open('../converted_nbs.pkl', 'r'))
    NCnbs_data = pickle.load(open('../NBS_noncovert.pkl', 'r'))
    emerge_artists = pd.read_sql('billboard_emerge', engine)
    main()