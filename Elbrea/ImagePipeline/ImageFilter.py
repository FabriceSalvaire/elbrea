####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

# from Elbrea.Image.Image import Image
# from Elbrea.Tools.EnumFactory import EnumFactory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TimeStamp(object):

    _time_stamp = 0

    ##############################################

    def __init__(self):

        self._modified_time = 0

    ##############################################

    def __lt__(self, other):
        return self._modified_time < other._modified_time

    ##############################################

    def __int__(self):
        return self._modified_time

    ##############################################

    def modified(self):

        # Should be atomic
        TimeStamp._time_stamp += 1
        self._modified_time = TimeStamp._time_stamp

####################################################################################################

class Object(object):

     ##############################################

    def __init__(self):

        self._modified_time = TimeStamp()

    ##############################################

    @property
    def modified_time(self):
        return int(self._modified_time)

    ##############################################

    def modified(self):

        self._modified_time.modified()

####################################################################################################

class ImageFilterOutput(Object):

    _logger = _module_logger.getChild('ImageFilterOutput')

    ##############################################

    def __init__(self, source, name):

        Object.__init__(self)

        self._update_time = TimeStamp()
        self._pipeline_time = 0
        self.connect_source(source, name)

    ##############################################

    @property
    def source(self):
        return self._source

    ##############################################

    @property
    def name(self):
        return "{}.{}".format(self._source.name, self._name)

    ##############################################

    @property
    def update_time(self):
        return self._update_time

    ##############################################

    @property
    def pipeline_time(self):
        return self._pipeline_time

    @pipeline_time.setter
    def pipeline_time(self, time):
        self._pipeline_time = time

    ##############################################

    def connect_source(self, source, name):

        self._source = source # image_filter
        self._name = name
        self.modified()

    ##############################################

    def disconnect_source(self):

        self._source = None
        self._name = None
        self.modified()

    ##############################################

    def update(self):

        self._logger.info(self.name)
        self.update_output_information()
        self.propagate_requested_region()
        self.update_output_data()

    ##############################################

    def update_output_information(self):

        self._logger.info(self.name)
        self._source.update_output_information()

    ##############################################

    def propagate_requested_region(self):

        self._logger.info(self.name)
        if int(self._update_time) < self._pipeline_time:
            self._source.propagate_requested_region(self)
            
        # self.verify_requested_region()

    ##############################################

    def update_output_data(self):

        self._logger.info(self.name)
        if int(self._update_time) < self._pipeline_time:
            self._source.update_output_data()

    ##############################################

    def copy_information(self, input_):

        self._logger.info("from {} to {}".format(input_.name, self.name))

    ##############################################

    def data_has_been_generated(self):

        self._logger.info(self.name)
        self.modified()
        self._update_time.modified()

####################################################################################################

class ImageFilter(Object):

    _last_filter_id = 0

    __filter_name__ = None
    __input_names__ = None
    __output_names__ = None

    _logger = _module_logger.getChild('ImageFilter')

    ##############################################

    @staticmethod
    def _new_filter_id():

        ImageFilter._last_filter_id += 1

        return ImageFilter._last_filter_id

    ##############################################

    def __init__(self):

        Object.__init__(self)

        self._filter_id = self._new_filter_id()
        self._output_information_time = TimeStamp()
        self._modified_time = TimeStamp()
        self.modified() 
        self._updating = False

        self._inputs = dict()
        self._outputs = {name:ImageFilterOutput(self, name) for name in self.__output_names__}

    ##############################################

    def __del__(self):

        for output in self._outputs.values():
            output.disconnect_source()

    ##############################################

    def __repr__(self):

        return self.__filter_name__

    ##############################################

    @property
    def name(self):
        return self.__filter_name__

    @property
    def input_names(self):
        return self.__input_names__

    @property
    def output_names(self):
        return self.__output_names__

    @property
    def filter_id(self):
        return self._filter_id

    ##############################################

    def get_input(self, name):
        return self._inputs[name]

    ##############################################

    def connect_input(self, name, source):

        self._inputs[name] = source

    ##############################################

    def disconnect_input(self, name):

        if name in self._inputs:
            del self._inputs[name]

    ##############################################

    def get_output(self, name):
        return self._outputs[name]
        
    ##############################################

    def get_primary_input(self):
        return self.get_input(self.__input_names__[0])

    ##############################################

    def get_primary_output(self):
        return self.get_output(self.__output_names__[0])

    ##############################################

    def update(self):

        self._logger.info(self.name)
        self.get_primary_output().update()

    ##############################################

    def update_output_information(self):

        self._logger.info(self.name)

        # Watch out for loops in the pipeline
        if self._updating:
            # Since we are in a loop, we will want to update. But if we don't modify this filter,
            # then we will not execute because our OutputInformationMTime will be more recent than
            # the MTime of our output.
            self.modified()
            return
            
        # Verify that the process object has been configured correctly, that all required inputs are
        # set, and needed parameters are set appropriately before we continue the pipeline, i.e. is
        # the filter in a state that it can be run.
        # self.verify_preconditions()
        for input_name in self.__input_names__:
            if input_name not in self._inputs:
                raise NameError("Input {} is required".format(input_name))

        # We now wish to set the PipelineMTime of each output DataObject to the largest of this
        # ProcessObject's MTime, all input DataObject's PipelineMTime, and all input's MTime.  We
        # begin with the MTime of this ProcessObject.
        modified_time = self.modified_time

        # Loop through the inputs
        for input_ in self._inputs.values():
            # Propagate the UpdateOutputInformation call
            self._updating = True
            input_.update_output_information()
            self._updating = False

            # What is the PipelineMTime of this input? Compare this against our current computation
            # to find the largest one.
            # Pipeline MTime of the input does not include the MTime of the data object
            # itself. Factor these mtimes into the next PipelineMTime
            modified_time = max(modified_time, input_.modified_time, input_.pipeline_time)

        # Call GenerateOutputInformation for subclass specific information.  Since
        # UpdateOutputInformation propagates all the way up the pipeline, we need to be careful here
        # to call GenerateOutputInformation only if necessary. Otherwise, we may cause this source
        # to be modified which will cause it to execute again on the next update.
        if modified_time > int(self._output_information_time):
            for output in self._outputs.values():
                output.pipeline_time = modified_time

            # Verify that all the inputs are consistent with the requirements of the filter. For
            # example, subclasses might want to ensure all the inputs are in the same coordinate
            # frame.
            # self.verify_input_information()

            # Finally, generate the output information.
            self.generate_output_information()

            # Keep track of the last time GenerateOutputInformation() was called
            self._output_information_time.modified()

    ##############################################

    def generate_output_information(self):

        self._logger.info(self.name)
        if self._inputs:
            primary_input = self.get_primary_input()
            for output in self._outputs.values():
                output.copy_information(primary_input)

    ##############################################

    def propagate_requested_region(self, output):

        self._logger.info(self.name)

        # check flag to avoid executing forever if there is a loop
        if self._updating:
            return

        # Give the subclass a chance to indicate that it will provide more data then required for
        # the output. This can happen, for example, when a source can only produce the whole output.
        # Although this is being called for a specific output, the source may need to enlarge all
        # outputs.
        # self.enlarge_output_requested_region(output)

        # Give the subclass a chance to define how to set the requested regions for each of its
        # outputs, given this output's requested region.  The default implementation is to make all
        # the output requested regions the same.  A subclass may need to override this method if
        # each output is a different resolution.
        # self.generate_output_requested_region(output)

        # Give the subclass a chance to request a larger requested region on the inputs. This is
        # necessary when, for example, a filter requires more data at the "internal" boundaries to
        # produce the boundary values - such as an image filter that derives a new pixel value by
        # applying some operation to a neighborhood of surrounding original values.
        # self.generate_input_requested_region()

        # Now that we know the input requested region, propagate this through all the inputs.
        self._updating = False
        for input_ in self._inputs.values():
            input_.propagate_requested_region()
        self._updating = False

    ##############################################

    def update_output_data(self):

        self._logger.info(self.name)

        # prevent chasing our tail
        if self._updating:
            return

        # Prepare all the outputs. This may deallocate previous bulk data.
        # self.prepare_outputs()

        # Propagate the update call - make sure everything we might rely on is up-to-date
        # Must call PropagateRequestedRegion before UpdateOutputData if multiple inputs since they
        # may lead back to the same data object.
        self._updating = True
        if len(self._inputs) == 1:
            self.get_primary_input().update_output_data()
        else:
            for input_ in self._inputs.values():
                # propagate_requested_region
                input_.update_output_data()

        # start
        self.generate_data()
        # stop

        # Now we have to mark the data as up to date.
        for output in self._outputs.values():
            output.data_has_been_generated()

        self._updating = False

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

####################################################################################################
# 
# End
# 
####################################################################################################
