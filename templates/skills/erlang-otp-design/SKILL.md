---
name: erlang-otp-design
description: Erlang/OTP 26+ supervision trees, map-based child specifications, GenServer callbacks, and fault-tolerant restarts.
author: "Erlang/OTP Community & ai-assist-bootstrap"
version: "1.0.0"
license: "Apache-2.0"
metadata:
  origin_repo: "https://github.com/erlang/otp"
  upstream_file: "system/doc/design_principles/README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "OTP 26 map-based child specifications"
    - "Clean gen_server callback separation"
    - "Dialyzer -spec type declarations"
---

# Erlang OTP 26+ Architecture Runbook

## When to Use
Use this skill when designing supervision trees, implementing `gen_server` processes, configuring OTP application specs, or organizing fault tolerance in Erlang OTP 26+.

---

## 1. OTP 26 Map-Based Supervisor Child Specifications

Always use map-based child specifications in `init/1`. Never use obsolete tuple syntax (`{Id, StartFunc, Restart, Shutdown, Type, Modules}`):

```erlang
-module(my_sup).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{
        strategy  => one_for_one,
        intensity => 3,
        period    => 10
    },
    ChildSpecs = [
        #{
            id       => my_worker,
            start    => {my_worker, start_link, []},
            restart  => permanent,
            shutdown => 5000,
            type     => worker,
            modules  => [my_worker]
        }
    ],
    {ok, {SupFlags, ChildSpecs}}.
```

---

## 2. GenServer Callback Safety

Follow strict separation between synchronous `handle_call` (must return `{reply, Reply, NewState}`) and asynchronous `handle_cast` (must return `{noreply, NewState}`):

```erlang
-module(my_worker).
-behaviour(gen_server).

-export([start_link/0, get_value/1, set_value/2]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

-record(state, {data = #{} :: map()}).

-spec start_link() -> {ok, pid()} | {error, term()}.
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

-spec get_value(Key :: term()) -> {ok, term()} | error.
get_value(Key) ->
    gen_server:call(?MODULE, {get, Key}).

-spec set_value(Key :: term(), Value :: term()) -> ok.
set_value(Key, Value) ->
    gen_server:cast(?MODULE, {set, Key, Value}).

init([]) ->
    {ok, #state{}}.

handle_call({get, Key}, _From, State) ->
    Reply = maps:find(Key, State#state.data),
    {reply, Reply, State};
handle_call(_Request, _From, State) ->
    {reply, {error, unknown_call}, State}.

handle_cast({set, Key, Value}, State) ->
    NewData = maps:put(Key, Value, State#state.data),
    {noreply, State#state{data = NewData}};
handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.
```

---

## 3. Supervision Restart Policies
- **`permanent`**: Child process is always restarted. Standard for core services.
- **`transient`**: Child is restarted only if it terminates abnormally. Standard for tasks meant to terminate naturally.
- **`temporary`**: Child is never restarted.

---

## 4. Verification & Dialyzer
- **Compile & Test**: `rebar3 eunit`
- **Static Type Analysis**: `rebar3 dialyzer`
- **Linting**: `rebar3 elvis rock`

