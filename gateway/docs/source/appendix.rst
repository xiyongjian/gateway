API Reference
-------------

Running a Backtest
~~~~~~~~~~~~~~~~~~

.. autofunction:: gateway.run_algorithm(...)

Algorithm API
~~~~~~~~~~~~~

The following methods are available for use in the ``initialize``,
``handle_data``, and ``before_trading_start`` API functions.

In all listed functions, the ``self`` argument is implicitly the
currently-executing :class:`~gateway.algorithm.TradingAlgorithm` instance.

Data Object
```````````

.. autoclass:: gateway.protocol.BarData
   :members:

Scheduling Functions
````````````````````

.. autofunction:: gateway.api.schedule_function

.. autoclass:: gateway.api.date_rules
   :members:
   :undoc-members:

.. autoclass:: gateway.api.time_rules
   :members:

Orders
``````

.. autofunction:: gateway.api.order

.. autofunction:: gateway.api.order_value

.. autofunction:: gateway.api.order_percent

.. autofunction:: gateway.api.order_target

.. autofunction:: gateway.api.order_target_value

.. autofunction:: gateway.api.order_target_percent

.. autoclass:: gateway.finance.execution.ExecutionStyle
   :members:

.. autoclass:: gateway.finance.execution.MarketOrder

.. autoclass:: gateway.finance.execution.LimitOrder

.. autoclass:: gateway.finance.execution.StopOrder

.. autoclass:: gateway.finance.execution.StopLimitOrder

.. autofunction:: gateway.api.get_order

.. autofunction:: gateway.api.get_open_orders

.. autofunction:: gateway.api.cancel_order

Order Cancellation Policies
'''''''''''''''''''''''''''

.. autofunction:: gateway.api.set_cancel_policy

.. autoclass:: gateway.finance.cancel_policy.CancelPolicy
   :members:

.. autofunction:: gateway.api.EODCancel

.. autofunction:: gateway.api.NeverCancel


Assets
``````

.. autofunction:: gateway.api.symbol

.. autofunction:: gateway.api.symbols

.. autofunction:: gateway.api.future_symbol

.. autofunction:: gateway.api.set_symbol_lookup_date

.. autofunction:: gateway.api.sid


Trading Controls
````````````````

Gateway provides trading controls to help ensure that the algorithm is
performing as expected. The functions help protect the algorithm from certian
bugs that could cause undesirable behavior when trading with real money.

.. autofunction:: gateway.api.set_do_not_order_list

.. autofunction:: gateway.api.set_long_only

.. autofunction:: gateway.api.set_max_leverage

.. autofunction:: gateway.api.set_max_order_count

.. autofunction:: gateway.api.set_max_order_size

.. autofunction:: gateway.api.set_max_position_size


Simulation Parameters
`````````````````````

.. autofunction:: gateway.api.set_benchmark

Commission Models
'''''''''''''''''

.. autofunction:: gateway.api.set_commission

.. autoclass:: gateway.finance.commission.CommissionModel
   :members:

.. autoclass:: gateway.finance.commission.PerShare

.. autoclass:: gateway.finance.commission.PerTrade

.. autoclass:: gateway.finance.commission.PerDollar

Slippage Models
'''''''''''''''

.. autofunction:: gateway.api.set_slippage

.. autoclass:: gateway.finance.slippage.SlippageModel
   :members:

.. autoclass:: gateway.finance.slippage.FixedSlippage

.. autoclass:: gateway.finance.slippage.VolumeShareSlippage

Pipeline
````````

For more information, see :ref:`pipeline-api`

.. autofunction:: gateway.api.attach_pipeline

.. autofunction:: gateway.api.pipeline_output


Miscellaneous
`````````````

.. autofunction:: gateway.api.record

.. autofunction:: gateway.api.get_environment

.. autofunction:: gateway.api.fetch_csv


.. _pipeline-api:

Pipeline API
~~~~~~~~~~~~

.. autoclass:: gateway.pipeline.Pipeline
   :members:
   :member-order: groupwise

.. autoclass:: gateway.pipeline.CustomFactor
   :members:
   :member-order: groupwise

.. autoclass:: gateway.pipeline.filters.Filter
   :members: __and__, __or__
   :exclude-members: dtype

.. autoclass:: gateway.pipeline.factors.Factor
   :members: bottom, deciles, demean, linear_regression, pearsonr,
             percentile_between, quantiles, quartiles, quintiles, rank,
             spearmanr, top, winsorize, zscore, isnan, notnan, isfinite, eq,
             __add__, __sub__, __mul__, __div__, __mod__, __pow__, __lt__,
             __le__, __ne__, __ge__, __gt__
   :exclude-members: dtype
   :member-order: bysource

.. autoclass:: gateway.pipeline.term.Term
   :members:
   :exclude-members: compute_extra_rows, dependencies, inputs, mask, windowed

.. autoclass:: gateway.pipeline.data.USEquityPricing
   :members: open, high, low, close, volume
   :undoc-members:

Built-in Factors
````````````````

.. autoclass:: gateway.pipeline.factors.AverageDollarVolume
   :members:

.. autoclass:: gateway.pipeline.factors.BollingerBands
   :members:

.. autoclass:: gateway.pipeline.factors.BusinessDaysSincePreviousEvent
   :members:

.. autoclass:: gateway.pipeline.factors.BusinessDaysUntilNextEvent
   :members:

.. autoclass:: gateway.pipeline.factors.ExponentialWeightedMovingAverage
   :members:

.. autoclass:: gateway.pipeline.factors.ExponentialWeightedMovingStdDev
   :members:

.. autoclass:: gateway.pipeline.factors.Latest
   :members:

.. autoclass:: gateway.pipeline.factors.MACDSignal
   :members:

.. autoclass:: gateway.pipeline.factors.MaxDrawdown
   :members:

.. autoclass:: gateway.pipeline.factors.Returns
   :members:

.. autoclass:: gateway.pipeline.factors.RollingLinearRegressionOfReturns
   :members:

.. autoclass:: gateway.pipeline.factors.RollingPearsonOfReturns
   :members:

.. autoclass:: gateway.pipeline.factors.RollingSpearmanOfReturns
   :members:

.. autoclass:: gateway.pipeline.factors.RSI
   :members:

.. autoclass:: gateway.pipeline.factors.SimpleMovingAverage
   :members:

.. autoclass:: gateway.pipeline.factors.VWAP
   :members:

.. autoclass:: gateway.pipeline.factors.WeightedAverageValue
   :members:

Built-in Filters
````````````````

.. autoclass:: gateway.pipeline.filters.All
   :members:

.. autoclass:: gateway.pipeline.filters.AllPresent
   :members:

.. autoclass:: gateway.pipeline.filters.Any
   :members:

.. autoclass:: gateway.pipeline.filters.AtLeastN
   :members:

.. autoclass:: gateway.pipeline.filters.SingleAsset
   :members:

.. autoclass:: gateway.pipeline.filters.StaticAssets
   :members:

.. autoclass:: gateway.pipeline.filters.StaticSids
   :members:

Pipeline Engine
```````````````

.. autoclass:: gateway.pipeline.engine.PipelineEngine
   :members: run_pipeline, run_chunked_pipeline
   :member-order: bysource

.. autoclass:: gateway.pipeline.engine.SimplePipelineEngine
   :members: __init__, run_pipeline, run_chunked_pipeline
   :member-order: bysource

.. autofunction:: gateway.pipeline.engine.default_populate_initial_workspace

Data Loaders
````````````

.. autoclass:: gateway.pipeline.loaders.equity_pricing_loader.USEquityPricingLoader
   :members: __init__, from_files, load_adjusted_array
   :member-order: bysource

Asset Metadata
~~~~~~~~~~~~~~

.. autoclass:: gateway.assets.Asset
   :members:

.. autoclass:: gateway.assets.Equity
   :members:

.. autoclass:: gateway.assets.Future
   :members:

.. autoclass:: gateway.assets.AssetConvertible
   :members:


Trading Calendar API
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: gateway.utils.calendars.get_calendar

.. autoclass:: gateway.utils.calendars.TradingCalendar
   :members:

.. autofunction:: gateway.utils.calendars.register_calendar

.. autofunction:: gateway.utils.calendars.register_calendar_type

.. autofunction:: gateway.utils.calendars.deregister_calendar

.. autofunction:: gateway.utils.calendars.clear_calendars


Data API
~~~~~~~~

Writers
```````
.. autoclass:: gateway.data.minute_bars.BcolzMinuteBarWriter
   :members:

.. autoclass:: gateway.data.us_equity_pricing.BcolzDailyBarWriter
   :members:

.. autoclass:: gateway.data.us_equity_pricing.SQLiteAdjustmentWriter
   :members:

.. autoclass:: gateway.assets.AssetDBWriter
   :members:

Readers
```````
.. autoclass:: gateway.data.minute_bars.BcolzMinuteBarReader
   :members:

.. autoclass:: gateway.data.us_equity_pricing.BcolzDailyBarReader
   :members:

.. autoclass:: gateway.data.us_equity_pricing.SQLiteAdjustmentReader
   :members:

.. autoclass:: gateway.assets.AssetFinder
   :members:

.. autoclass:: gateway.data.data_portal.DataPortal
   :members:

Bundles
```````
.. autofunction:: gateway.data.bundles.register

.. autofunction:: gateway.data.bundles.ingest(name, environ=os.environ, date=None, show_progress=True)

.. autofunction:: gateway.data.bundles.load(name, environ=os.environ, date=None)

.. autofunction:: gateway.data.bundles.unregister

.. data:: gateway.data.bundles.bundles

   The bundles that have been registered as a mapping from bundle name to bundle
   data. This mapping is immutable and should only be updated through
   :func:`~gateway.data.bundles.register` or
   :func:`~gateway.data.bundles.unregister`.


Utilities
~~~~~~~~~

Caching
```````

.. autoclass:: gateway.utils.cache.CachedObject

.. autoclass:: gateway.utils.cache.ExpiringCache

.. autoclass:: gateway.utils.cache.dataframe_cache

.. autoclass:: gateway.utils.cache.working_file

.. autoclass:: gateway.utils.cache.working_dir

Command Line
````````````
.. autofunction:: gateway.utils.cli.maybe_show_progress
