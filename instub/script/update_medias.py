#! -*- coding: utf-8 -*-

import sys
sys.path.append('../../')

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.database import get_last_media, get_instub_token, insert_medias


def get_instub_feed(access_token, min_id=None):
    print min_id
    try:
        api = InstagramAPI(access_token=access_token)
        medias_list = []
        next_ = True
        while next_:
            next_url = None if next_ is True else next_
            medias, next_ = api.user_media_feed(with_next_url=next_url,
                                                min_id=min_id)
            medias_list.extend(medias)
        return medias_list
    except InstagramAPIError, e:
        if e.error_type in ['APINotAllowedError-you',
                            'APINotFoundError-this']:
            pass
        return []


def update_workers_media():
    access_token = get_instub_token(fetchone=True)
    if not access_token:
        return
    min_id = get_last_media()
    medias = get_instub_feed(access_token=access_token, min_id=min_id)
    if medias:
        insert_medias(medias[:-1])


def main():
    import time
    while True:
        update_workers_media()
        time.sleep(300)
        print time.time()


if __name__ == '__main__':
    main()
