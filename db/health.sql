SELECT
    hnm.id AS menu_id,
    hnm.menu_week_id,
    hnm.day_of_week,
    hn_breakfast.name AS breakfast_name,
    hn_breakfast_snack.name AS breakfast_snack_name,
    hn_lunch.name AS lunch_name,
    hn_afternoon_snack.name AS afternoon_snack_name,
    hn_dinner.name AS dinner_name,
    hn_night_snack.name AS night_snack_name
FROM
    health_nutrition_menu hnm
INNER JOIN
    health_nutrition hn_breakfast ON hnm.breakfast_id = hn_breakfast.id
INNER JOIN
    health_nutrition hn_breakfast_snack ON hnm.breakfast_snack_id = hn_breakfast_snack.id
INNER JOIN
    health_nutrition hn_lunch ON hnm.lunch_id = hn_lunch.id
INNER JOIN
    health_nutrition hn_afternoon_snack ON hnm.afternoon_snack_id = hn_afternoon_snack.id
INNER JOIN
    health_nutrition hn_dinner ON hnm.dinner_id = hn_dinner.id
INNER JOIN
    health_nutrition hn_night_snack ON hnm.night_snack_id = hn_night_snack.id;