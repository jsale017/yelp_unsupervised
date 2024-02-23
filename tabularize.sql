CREATE OR REPLACE TABLE `ba820-proj.yelp_academic_dataset.tabularized` AS (
  SELECT *
  FROM `ba820-proj.yelp_academic_dataset.reviews` reviews
  LEFT JOIN (
    SELECT user_id, average_stars AS average_user_stars, yelping_since, review_count AS submitted_reviews
    FROM `ba820-proj.yelp_academic_dataset.users`
  ) USING (user_id)
  LEFT JOIN (
    SELECT business_id, name, address, city, state, postal_code latitude, longitude, stars AS average_business_stars, review_count AS recieved_reviews, categories, attributes
    FROM `ba820-proj.yelp_academic_dataset.businesses`
  ) USING (business_id)
  LEFT JOIN (
    SELECT user_id, business_id, text AS tip_review
    FROM `ba820-proj.yelp_academic_dataset.tips`
  ) USING (business_id, user_id)
)