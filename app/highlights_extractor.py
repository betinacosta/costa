from gmail_client import GmailClient


def main():
    client = GmailClient()

    service = client.authenticate()

    # message_list = client.get_messages_matching_query(service, "from:no-reply@amazon.com has:attachment")

    # message = client.get_message_details(service, "16e395b3b1ff9e44")

    client.download_attachment(service, "16e395b3b1ff9e44", "ANGjdJ-zj8NeFS5WDxU4gQ54xHPMZxpScOjRb4pw2_7KM--Jb_7e2rWRutqma1VQW-lCeKD0hs5XPehNOPYT3V4u9dL0cj26_WObMOivb08ID6Z1UemxA8HVWiw5ts4x-YELH6IWgs848Pk7G_60uyjiAcs_2yE5NeOhV22_--JTJ3TyMiyRL3KikmbtrHHkixLsA03IVfgCCdKMVaPHEd6-R00IQo3-AE_vyDsPkPnyLi2AWPQ33YLHTYniC8eHfH2ahPyYzCjelRhEZ9qEvdyI5W2b7GOdIcFXoNiMLr5ThXajOelosNrUMhfsJcD_VHrlbArd_R-l6I13tdIcqpUqJmOETjqRiGJr6Pr-rCN6UiejNLoP8xnHagRbvAc")



    # print(message)


if __name__ == '__main__':
    main()
