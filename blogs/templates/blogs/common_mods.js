$load("favourite_posts","{% url 'blogs:favourite_posts_mod' lawyer.id %}");
$load("all_cats","{% url 'blogs:categories_mod' lawyer.id %}?e={{is_master}}");
$load("recent_comments","{% url 'blogs:recent_comments_mod' lawyer.id %}");
$load("tags_cloud","{% url 'blogs:tags_mod' lawyer.id %}");
