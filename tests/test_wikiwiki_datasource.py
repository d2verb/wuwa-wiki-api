from src.data_source.wikiwiki import WikiWikiDataSource, WikiWikiHttpClient

class TestWikiWikiDatasource:
    def test_get_resonators(self):
        class MockHttpClient:
            def get_page_source(self, page_title: str) -> str | None:
                return """*共鳴者一覧 [#list]
#tablesort{{
|&nobr{画像};|&nobr{&nbsp;名前&nbsp;};|ﾚｱ|
|SIZE(5):CENTER:BGCOLOR(#333):55|CENTER:|
|[[&ref(画像/カンタレラ.webp,nolink,48x48);>カンタレラ]]|[[カンタレラ]]|
|[[&ref(画像/フィービー.webp,nolink,48x48);>フィービー]]|[[フィービー]]|
|&ref(画像/カルテジア.webp,nolink,48x48);|カルテジア|
|[[&ref(画像/吟霖.webp,nolink,48x48);>吟霖]]|[[&ruby(インリン){吟霖};>吟霖]]|
|[[&ref(画像/ビャクシ.webp,nolink,48x48);>ビャクシ]]|[[&ruby(ビャクシ){白&#33463;};>ビャクシ]]|
|[[&ref(画像/漂泊者_気動.webp,nolink,48x48);>漂泊者]]|[[漂泊者&br;(気動)>漂泊者（気動）]]|
}}
"""

        client = MockHttpClient()
        datasource = WikiWikiDataSource(client)
        resonators = datasource.get_resonators()
        assert len(resonators) == 6
        assert resonators[0] == "カンタレラ"
        assert resonators[1] == "フィービー"
        assert resonators[2] == "カルテジア"
        assert resonators[3] == "吟霖"
        assert resonators[4] == "ビャクシ"
        assert resonators[5] == "漂泊者（気動）"
