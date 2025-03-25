from flask import Flask, render_template
import vk_api
import datetime

app = Flask(__name__)


@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return f"AuthError: {error_msg}"
    vk = vk_session.get_api()

    stats_data = vk.stats.get(group_id=group_id, fields="reach", intervals_count=10)

    activity_sum = {
        "likes": 0,
        "comments": 0,
        "subscribed": 0
    }
    ages_sum = {}
    cities_sum = {}

    for period in stats_data:
        if "activity" in period and period["activity"]:
            activity_sum["likes"] += period["activity"].get("likes", 0)
            activity_sum["comments"] += period["activity"].get("comments", 0)
            activity_sum["subscribed"] += period["activity"].get("subscribed", 0)

        if "reach" in period and period["reach"]:
            if "age" in period["reach"]:
                for age_obj in period["reach"]["age"]:
                    age_val = age_obj.get("value")
                    count = age_obj.get("count", 0)
                    if age_val:
                        ages_sum[age_val] = ages_sum.get(age_val, 0) + count

            if "cities" in period["reach"]:
                for city_obj in period["reach"]["cities"]:
                    city_val = city_obj.get("value")
                    count = city_obj.get("count", 0)
                    if city_val:
                        cities_sum[city_val] = cities_sum.get(city_val, 0) + count

    return render_template(
        "vk_stat.html",
        activity_sum=activity_sum,
        ages_sum=ages_sum,
        cities_sum=cities_sum
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
