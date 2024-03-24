from justsubs import Video

# Сейчас dict_from_text() возвращает список строк, должен возвращать
# словарь c ключами в виде меток времени, когда начинается блок,
# и содержанием блока в виде строки или списка строк.
# Также сейчас метки времени для блока расставляются неверно.
# Должен проходить тест test_blocks_new_behavior()
# Тест по согласованию может быть уточнен.
# Результат - PR в этот репо.


def test_blocks_new_behavior():
    subtitles = Video("gBnLl3QBOdM").vtt("en").download()
    vtt_text = subtitles.filename.read_text(encoding="utf-8")
    assert dict_from_text(vtt_text) == {
        "00:09": """our initial idea was to extend some of the heavily researched ideas on spot and
forward contracting foreign exchange and
and extend them to to analyze volatility instead of the level of the exchange
rates at the basic idea is that the forward market if if markets are
efficient it should it should be providing us with expectation of where
the exchange rate is going in the future which are correct on average now that
simple hypothesis has been heavily tested for over 30 years ever since
Eugene fama and Chicago started working in this area and what we know about that""",
        "00:54": """relationship is that the forward market does not provide unbiased expectations
of the future exchange rates so there's no providers with any evidence that the
basic theory behind this relation is is correct now we extend these ideas to the
volatility market and this is really exciting because in the last 10 years
there has been an explosion of contracts derivatives contracts which essentially
allow us to trade the volatility of an exchange rate as opposed to trading the
exchange rate itself under the same assumptions is standard the market
efficiency and risk neutrality behind forward unbiasness we would expect that
the forward market for volatility contracts provides us with an unbiased
expectation of where volatility goes in the future in other words with an
expectation which is correct on average and what we find is that this basic
theory it is basic forward unbiasness hypothesis which return the forward""",
        "01:58": """volatility unbiased and a psychologist is rejected by the data just like the
standard combines and psychologist is rejected in the conventional spot and
forward market for foreign exchange and that forward bias gives rise to a risk
premium which we quantify in this research so in addition to providing
statistical evidence that documents the rejection of this
basic theory more importantly we find the evidence that these statistical
findings are economically very important
because the risk premium are rising as a consequence of these biases is very
large most striking part of this new risk premium it's a century of
volatility tolerant premium is that it appears to be very different from any
other risk premium in the in the foreign exchange market so it's not correlated
with the traditional risk premium it's also not correlated with the other""",
        "02:57": """conventional risk premia that we know about in asset markets so in a sense we
think we found a source of risk adjusted returns for us and managers that is new
is coming from a different kind of anomaly if you want that we didn't know
about before""",
    }
