from unittest.mock import patch, call, Mock

import pytest

from domination import process


@pytest.fixture()
def fixture_faust_app(event_loop):
    process.app.finalize()
    process.app.conf.store = 'memory://'
    process.app.flow_control.resume()
    return process.app


@pytest.mark.asyncio
async def test_detect_human_type_call_process():
    """Assert agent process human_rating"""

    with patch('domination.process.process_human_rating') as mock_process_human, \
            patch('domination.process.shadow_topic') as mock_shadow_topic:
        mock_shadow_topic.send = mock_corotine()
        async with process.detect_human_type.test_context() as agent:
            human = process.HumanRating(rating=18, unique_id="unique_123")
            await agent.put(human)
            assert mock_process_human.mock_calls == [(call(human))]


@pytest.mark.asyncio
async def test_detect_human_type_send_topic():
    """Assert agent send human_categorized to 'shadow' topic"""

    with patch('domination.process.shadow_topic') as mock_shadow_topic:
        mock_shadow_topic.send = mock_corotine()
        async with process.detect_human_type.test_context() as agent:
            human = process.HumanRating(rating=18, unique_id="unique_123")
            await agent.put(human)

            human_categorized = process.HumanCategorized(unique_id=human.unique_id, type='Sha')
            assert mock_shadow_topic.send.mock_calls == [(call(value=human_categorized))]


@pytest.mark.asyncio
async def test_detect_human_type_error():
    """Rating as string -> raises error"""

    with patch('domination.process.shadow_topic') as mock_shadow_topic, \
            patch('logging.error') as mocked_logging_error:
        mock_shadow_topic.send = mock_corotine()
        async with process.detect_human_type.test_context() as agent:
            human = process.HumanRating(rating='string', unique_id="unique_123")
            await agent.put(human)
            assert mock_shadow_topic.send.mock_calls == []
            mocked_logging_error.assert_called_with('Error: %s', 'human rating is not an integer')


# @pytest.mark.asyncio
# async def test_producer_of_humans():
#     """"""
#
#     with patch('domination.process.dominate_topic') as mock_dominate_topic_topic:
#         mock_dominate_topic_topic.send = mock_corotine()
#         result = process.producer_of_humans()
#         await result
#         print(mock_dominate_topic_topic.send.mock_calls)
#         assert len(mock_dominate_topic_topic.send.mock_calls) == 10
#         assert isinstance(mock_dominate_topic_topic.send.mock_calls[0].rating, int)
#         assert isinstance(mock_dominate_topic_topic.send.mock_calls[0].unique_id, str)


def mock_corotine(return_value=None, **kwargs):
    """Create mock coroutine function."""

    async def wrapped(*args, **kwargs):
        return return_value

    return Mock(wraps=wrapped, **kwargs)
