$load("favourite_posts","{% url 'blogs:favourite_posts_mod' lawyer.id %}");
$load("all_cats","{% url 'blogs:categories_mod' lawyer.id %}?e={{is_master}}");
$load("archives","{% url 'blogs:archives_mod' lawyer.id %}");
$load("recent_comments","{% url 'blogs:recent_comments_mod' lawyer.id %}");
$load("tags_cloud","{% url 'blogs:tags_mod' lawyer.id %}");
search_action("{% url 'blogs:search' lawyer.id %}");
