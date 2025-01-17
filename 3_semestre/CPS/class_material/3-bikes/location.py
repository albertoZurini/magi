import math

import matplotlib.pyplot as plt

import pandas as pd

import geopy.distance


class Location:
    def __init__(self, index, name, coordinates, traces):
        self.index = index
        self.name = name
        self.coordinates = coordinates
        self.traces = traces

    def distance(self, other):
        left = self.coordinates
        right = other.coordinates
        return geopy.distance.distance(left, right).m

    def get_trace_values(self):
        return [[value[1], value[2]] for value in self.traces]

    def get_trace_time(self):
        return [value[0] for value in self.traces]

    def __str__(self):
        return f"[{self.index},{self.coordinates}]"
    
    def __repr__(self):
        return self.__str__()


"""
Location database: use `generate_from_df` to generate a location database from a dataframe
"""
class LocationDatabase:
    def __init__(self):
        """
        Initialize an empty location database
        """
        self.db = list()

    @staticmethod
    def get_location_full(df: pd.DataFrame, name, index: int):
        """
        Get a location from a dataframe
        :param df: dataframe with the required columns
        :param name: name of the location
        :param index: index of the location
        :return: a location object
        """
        location = df[df['NAME'] == name]
        row = location.iloc[0]
        coordinates = row['LAT'], row['LONG']
        traces = location.apply(lambda row: (
            row['ABS_TIME'], row['NBBIKES'], row['NBEMPTYDOCKS']), axis=1)
        values = list(traces.values)
        values.sort(key=lambda x: x[0])
        return Location(index, name, coordinates, values)

    def generate_from_df(self, df: pd.DataFrame):
        """
        Generate a location database from a dataframe
        :param df: dataframe with the following columns:
            - NAME: location name
            - LAT: latitude
            - LONG: longitude
            - ABS_TIME: timestamp
            - NBBIKES: number of bikes
        """
        location_names = df['NAME'].unique()
        for n, name in enumerate(location_names):
            self.db.append(self.get_location_full(df, name, n))

    def generate_graph(self):
        """
        Generate a moonlight graph from the location database.
        The graph is a list of triples (i, j, d) where i and j are the indices of the locations and d is the distance between them.
        :return: a list of graphs for any time point in which it changes (if it never changes, the list will have only one graph)
        """
        graph = []
        for l_idx in range(len(self.db)):
            for r_idx in range(len(self.db)):
                left_location = self.db[l_idx]
                right_location = self.db[r_idx]
                graph.append([left_location.index, right_location.index,
                             left_location.distance(right_location)])
        return [graph]

    def get_traces(self):
        return [location.get_trace_values() for location in self.db]

    def get_time(self):
        return self.db[0].get_trace_time()

    def show_locations_map(self):
        self._scatter_plot()
        plt.show()

    def plot_results(self, robustness: [[[float]]], time_point:int):
        values = self.get_temporal_snapshot(robustness, time_point)
        self._scatter_plot([value[1] for value in values])
        plt.title(f"Rob/Sat at time {values[0][0]}")
        plt.legend()
        plt.show()

    def _scatter_plot(self, values=None):
        coordinates = [location.coordinates for location in self.db]
        lat = [x[0] for x in coordinates]
        long = [x[1] for x in coordinates]
        
        if(values is not None):
            colors = ["red" if value < 0 else "green" for value in values]
            abs_values = [500*abs(value) for value in values]
            plt.scatter(lat, long, c=colors, s=abs_values)
        else:
            plt.scatter(lat, long, c="black")

        print("lat", min(lat), max(lat))
        print("long", min(long), max(long))
    
    def __str__(self):
        return str([str(location) for location in self.db])
    
    def get_temporal_snapshot(self, result: [[[int]]], time: int):
        """
        :param result: the result of the monitoring shaped as [times] x [locations] x [trace], and the trace is [timestamp, satisfaction/robustness value]
        """
        return [location[time] for location in result]
