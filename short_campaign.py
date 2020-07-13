import datetime

import action_day
import create_dates
import create_posters
import organise_polling_day
import targetted_letter
import trello_utility
import ward_newsletter
from start_up import boot


def produce_short_campaign():
    client, main_board = boot()

    ost_board = client.get_board('9WVxzf50')
    cowley_board = client.get_board('146gQMLj')
    dsm_board = client.get_board('rsKD2538')
    test_board = client.get_board('Tc4kcuCu')


    # Cowley
    # 28th March
    # 12th April
    # 2nd / 3rd May
    action_day.create_action_day(datetime.date(year=2020, month=3, day=28), cowley_board, 'Cowley')
    action_day.create_action_day(datetime.date(year=2020, month=4, day=12), cowley_board, 'Cowley')
    action_day.create_action_day(datetime.date(year=2020, month=5, day=2), cowley_board, 'Cowley')

    action_day.create_action_day(datetime.date(year=2020, month=3, day=14), dsm_board, 'D&SM')
    action_day.create_action_day(datetime.date(year=2020, month=4, day=19), dsm_board, 'D&SM')
    action_day.create_action_day(datetime.date(year=2020, month=5, day=2), dsm_board, 'D&SM')

    action_day.create_action_day(datetime.date(year=2020, month=3, day=8), ost_board, 'Osney')
    action_day.create_action_day(datetime.date(year=2020, month=4, day=4), ost_board, 'Osney')
    action_day.create_action_day(datetime.date(year=2020, month=5, day=2), ost_board, 'Osney')

    # produce_short_campaign_internal(dsm_board)
    # produce_short_campaign_internal(cowley_board)
    # produce_short_campaign_internal(ost_board)

    # for board in (dsm_board, cowley_board, ost_board):
    #     goal = ward_newsletter.create_short_campaign_literature(delivery_date=datetime.date(year=2020, month=5, day=4),
    #                                                             board=board, custom_name='Vote Green Postcard',
    #                                                             description='An A5 post card with the three key messages. '
    #                                                                         'Delivered o the final week before polling day')
    #
    #     literatue_card = next(card for card in board.get_cards() if card.name == 'Produce short campaign literature')
    #     literatue_card.checklists[0].add_checklist_item(goal.url)

    # mosque_leaflet = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=5,
    #                                                                              day=1), dsm_board,
    #                                                                'Mosque leaflet',
    #                                                                'Small A5 leaflet to be handed outside mosques '
    #                                                                'after Friday prayers')


def produce_short_campaign_internal(board):
    print('Producing short campaign for ' + board.name)

    create_dates.create_date(board, datetime.date(year=2020, month=5, day=6), 'POLLING EVE')
    create_dates.create_date(board, datetime.date(year=2020, month=5, day=7), 'POLLING DAY')

    # create_dates.create_dates(board, datetime.date(year=2020, month=5, day=11),
    #                           datetime.date(year=2020, month=7, day=6), 7)
    #
    # short_campaign_literature = []
    #
    # # transition ward newsletter
    # transition_ward_newsletter = ward_newsletter.create_short_campaign_literature(
    #     datetime.date(year=2020, month=3, day=29), board, 'Transition Ward Newsletter',
    #     'Leaflet in style of regular ward newsletter, but in full colour. Should introduce the candidates. It should '
    #     'included the three key messages. ')
    # # posters
    # posters = create_posters.create_posters(datetime.date(year=2020, month=3, day=1), board)
    # short_campaign_literature.append(posters)
    #
    # out_cards, _ = ward_newsletter.create_goal_card('Short campaign out cards', board,
    #                                                 datetime.date(year=2020, month=3, day=1))
    # short_campaign_literature.append(out_cards)
    #
    # # letter to voters
    # targetted_letter = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=4,
    #                                                                                   day=5), board, 'Addressed letter',
    #                                                                     'Letter to all voters in handwritten font. '
    #                                                                     'Should be from the lead candidate explaining '
    #                                                                     'why they want to be councillor.')
    # short_campaign_literature.append(targetted_letter)
    #
    # map_leaflet = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=4,
    #                                                                              day=12), board, 'A3 Map Leaflet',
    #                                                                'A3 leaflet. One side a map of the ward with lots '
    #                                                                'of pictures. Other side a Green text on white '
    #                                                                'poster of the candidates. ')
    # short_campaign_literature.append(map_leaflet)
    #
    # letter_to_pv = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=4, day=19), board,
    #                                                                 'Vote Green Card for Postal Voters',
    #                                                                 'Post card with three messages on why should vote '
    #                                                                 'Green today. ')
    # short_campaign_literature.append(letter_to_pv)
    #
    # endorsement_leaflet = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=4,
    #                                                                                      day=26), board,
    #                                                                        'Endorsement leaflet',
    #                                                                        'A4 leaflet with local endorsements of the '
    #                                                                        'candidate.')
    # short_campaign_literature.append(endorsement_leaflet)
    #
    # lab_squeeze = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=5,
    #                                                                              day=2), board,
    #                                                                'Labour Squeeze leaflet',
    #                                                                'Letter to L3s explaining why they should '
    #                                                                'vote Green this time.')
    # short_campaign_literature.append(lab_squeeze)
    #
    # ld_squeeze = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=5,
    #                                                                             day=2), board,
    #                                                               'LD Squeeze leaflet',
    #                                                               'Letter to LD3/4s explaining why they should vote '
    #                                                               'Green this time. This should only be done if there '
    #                                                               'is capacity and/or >100 LDs on the canvassing '
    #                                                               'sheet.')
    # short_campaign_literature.append(ld_squeeze)
    #
    # school_leaflet = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=4,
    #                                                                                 day=30), board,
    #                                                                   'School leaflet',
    #                                                                   'A5 leaflet to be handed out before school starts at relevant schools.')
    # short_campaign_literature.append(school_leaflet)
    #
    # thank_you_ward_letter = ward_newsletter.create_short_campaign_literature(datetime.date(year=2020, month=6,
    #                                                                                        day=1), board,
    #                                                                          'Thank you ward newsletter',
    #                                                                          'Ward newsletter style (riso) with '
    #                                                                          'election results. Thank voters for '
    #                                                                          'voting Green. ')
    # short_campaign_literature.append(thank_you_ward_letter)
    #
    # produce_short_camp_lit, _ = ward_newsletter.create_goal_card('Produce short campaign literature', board,
    #                                                              datetime.date(year=2020, month=3, day=1))
    # produce_short_camp_lit.set_description(
    #     "Create all the literature for the short campaign in Feb so it just needs tweaks / printing in the short "
    #     "campaign. ")
    # produce_short_camp_lit.add_checklist('TODO', list(map(lambda lit: lit.url, short_campaign_literature)))

    canvassing_script = ward_newsletter.create_task_card('Produce canvassing script', board, datetime.date(2020, 2, 1),
                                                         datetime.date(2020, 2, 28),
                                                         "Create  a script for shot campaign canvassing. It should "
                                                         "include targeted responses for people who say they are "
                                                         "voting LAB / LD / CON. It should also contain short summary "
                                                         "information about any topical issues.")
    nominations = ward_newsletter.create_task_card('Collect nominations', board, datetime.date(2020, 3, 31),
                                                   datetime.date(2020, 4, 8),
                                                   "Collect 10 signatures from people in the ward. Must be submitted "
                                                   "by 4pm Wednesday 8th April")
    pv_check = ward_newsletter.create_task_card('Finish PV canvassing', board, datetime.date(2020, 4, 6),
                                                datetime.date(2020, 4, 26),
                                                "Verify that all postal voters have been canvassed. If not, priotise "
                                                "just postal voters in canvassing until all done. ")

    committee_room = organise_polling_day.organise_polling_day(board)

    eve_of_poll = ward_newsletter.create_eve_of_poll(datetime.date(year=2020, month=5, day=7), board)

    # box counting


produce_short_campaign()
