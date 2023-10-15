import streamlit as st
import preprocessor , helper
import matplotlib.pyplot as plt


st.sidebar.title('whatsapp chat analyzer')

# st.header('hello')


uploaded_file = st.sidebar.file_uploader('choose a file')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode('utf-8')
    # st.text(data)

    df = preprocessor.preprocess(data)

    # df.info
    # st.dataframe(df)

    # df.info()


    # fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('show analysis wrt', user_list)


    if st.sidebar.button('show Analysis'):
        
        num_messages , words , num_media , links = helper.fetch_stats(selected_user , df)
        st.title('top_statistics')        
        col1 , col2 , col3 , col4  = st.columns(4)  


        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')

            st.title(words)


        with col3:
            st.header('total media')

            st.title(num_media)

        with col4:
            st.header('total links')

            st.title(links)


        st.title('Month TImeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig , ax = plt.subplots()

        ax.plot(timeline['time'] , timeline['message'] , color = 'orange')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig , ax = plt.subplots()

        ax.plot(daily_timeline['only_date'] , daily_timeline['message'] , color = 'black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        st.title('Activity map')

        col1 , col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user , df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index , busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy Month')
            busy_month = helper.month_activity_map(selected_user , df)
            fig , ax = plt.subplots()
            ax.bar(busy_month.index , busy_month.values , color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':

            st.title('Most Busy Users')
            x , new_df = helper.most_busy_users(df)

            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index , x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        

        st.title('WordCloud')
        df_wc = helper.create_word_cloud(selected_user , df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)

        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user , df)

        fig ,ax = plt.subplots()
        ax.bar(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('most_common_Word')
        st.pyplot(fig)

        # st.dataframe(most_common_df)