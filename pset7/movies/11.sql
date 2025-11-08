SELECT movies.title
FROM stars
JOIN people ON people.id = stars.person_id
JOIN movies ON movies.id = stars.movie_id
JOIN ratings ON movies.id = ratings.movie_id
WHERE name LIKE '%Chadwick Boseman%'
ORDER BY rating DESC
LIMIT 5
