            login_sinta(page, username_sinta, password_sinta)
            target_url_sinta = 'https://sinta.kemdikbud.go.id/affiliations/profile/1093?page=110&view=scopus'
            article_links, article_years = get_article_links(page, target_url_sinta, num_pages)
            print(article_links)
            print(article_years)
            if article_links: