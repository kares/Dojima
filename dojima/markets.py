# Dojima, a markets client.
# Copyright (C) 2012  Emery Hemingway
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore

import dojima.model.commodities


class MarketsContainer(object):

    """ A container for containers that hold ExchangeProxys.

        Each ExchangeProxy may contain multiple markets.
    """

    def __init__(self):
        self.markets = dict()

    def __iter__(self):
        return list(self.markets.values()).__iter__()

    def __len__(self):
        return len(self.markets)

    def addExchange(self, exchange_proxy, local_pair, local_base_id, local_counter_id):
        base, counter = local_pair.split('_')
        b_row, c_row = dojima.model.commodities.local_model.getRows(local_base_id,
                                                                    local_counter_id)
        if (b_row is None) or (c_row is None):
            return
        
        if local_pair in self.markets:
            container = self.markets[local_pair]
        else:
            container = MarketProxy(local_pair)
            self.markets[local_pair] = container
        container.append(exchange_proxy)


class MarketProxy(object):

    def __init__(self, marketPair):
        self.exchanges = list()
        self.pair = marketPair
        self.base_id, self.counter_id = marketPair.split('_')

    def append(self, exchangeProxy):
        self.exchanges.append(exchangeProxy)

    def getPrettyName(self):
        base, counter = dojima.model.commodities.local_model.getNames(self.base_id, self.counter_id)
        return QtCore.QCoreApplication.translate('MarketProxy', "{0} / {1}", 
                                                 "{0} is the user specified name of the base commodity, and {1} is the counter,"
                                                 "you just pick the order and the seperator.").format(base, counter)

    def getPrecisionCounter(self):
        return dojima.model.commodities.local_model.getPrecision(self.counter_id)
    
    def getPrecisionBase(self):
       return dojima.model.commodities.local_model.getPrecision(self.base_id)

    def getPrecisionCounter(self):
        return dojima.model.commodities.local_model.getPrecision(self.counter_id)

    def getPrefixSuffixBase(self):
        return dojima.model.commodities.local_model.getPrefixSuffix(self.base_id)
            
    def getPrefixSuffixCounter(self):
        return dojima.model.commodities.local_model.getPrefixSuffix(self.counter_id)

    def getPrettyCommodityNames(self):
        return dojima.model.commodities.local_model.getNames(self.base_id, self.counter_id)
        
    def __iter__(self):
        return self.exchanges.__iter__()

    def __len__(self):
        return len(self.exchanges)

    def __str__(self):
        return self.pair


container = MarketsContainer()
