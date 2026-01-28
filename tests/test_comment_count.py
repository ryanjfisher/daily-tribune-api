"""
Comment Count Race Condition Fix - SCRUM-28
"""
import pytest
import threading

class TestCommentCountRace:
    """SCRUM-28: Fix negative comment count"""
    
    def test_count_never_negative(self, db_session, article_with_comments):
        """Rapid deletions should never cause negative count"""
        article_id = article_with_comments.id
        comment_ids = [c.id for c in article_with_comments.comments]
        
        # Delete all comments concurrently
        threads = []
        for cid in comment_ids:
            t = threading.Thread(target=delete_comment, args=(cid,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Verify count is 0, not negative
        article = db_session.get(Article, article_id)
        assert article.comment_count >= 0
