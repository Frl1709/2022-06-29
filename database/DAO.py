from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getNodes(n):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId, Title, ArtistId, count(*) as nTrack, sum(t.Milliseconds) as Durata
                    from track t, album a 
                    where a.AlbumId  = t.AlbumId 
                    group by a.AlbumId 
                    having nTrack > %s"""
        cursor.execute(query, (n,))
        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result
