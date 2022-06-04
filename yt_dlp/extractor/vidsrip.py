from .common import InfoExtractor

class VidsRipIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(?P<host>((piss|spy|jav)rip\.net)|((desper|poop)\.vids\.rip))/([a-z0-9-]+)/(?P<id>[0-9]+)[a-z0-9\.-]*'
    _TESTS = [{
        'url': 'https://pissrip.net/pissjapantv/26581-more-pretty-peepee-potty-girls.html',
        'md5': '07e214f6b6f8c66dbbcec6d9d4c69a19',
        'info_dict': {
            'id': '26581',
            'ext': 'mp4',
            'title': 'More Pretty Peepee Potty Girls',
            'description': str,
            'uploader': 'shewdew',
            'thumbnail': r're:^https?://.*\.jpg$',
            'age_limit': int,
        }
    }]

    def _real_extract(self, url):
        host = self._match_valid_url(url).group('host')
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        frame_url = 'https://' + host + '/player/player_us.php?news_id=' + video_id
        frame_url2 = 'https://' + host + '/player2/player_us.php?news_id=' + video_id
        frame_page = self._download_webpage(frame_url2, video_id, fatal=False)
        if frame_page is False:
            frame_page = self._download_webpage(frame_url, video_id)

        m3u8_url = self._html_search_regex(r'<source src="(.+)" type', frame_page, 'video_url', fatal=False)
        formats = self._extract_m3u8_formats(
            m3u8_url, video_id, 'mp4', 'm3u8_native', m3u8_id='hls',
            note='Downloading m3u8 information', errnote='Unable to download m3u8 information')

        uploader = self._html_search_regex(
            r'href="https://[a-z\.]+/user/([0-9A-Za-z-]+?)/?"', webpage,
            'uploader', fatal=False)

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            'uploader': uploader,
            'age_limit': 18,
            'formats': formats,
        }
