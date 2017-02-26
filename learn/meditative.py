from tensorflow import tf

def extract_data(filename):

	#arrays to hold label and feature
	labels = []
	fvecs = []

	for line in file(filename):
		row = line.split(',')
		labels.append(int(row[0]))
		fvecs.append([float(x) for x in row[1:2]])


	#convert the array of float to numpy float matrix
	fvecs_np = np.matrix(fvecs.astype(np.float32)


	#convert the array of int labels into numpy array
	labels_np = np.array(labels).astype(dtype=np.uint8)

	#convert the int numpy array into one-hot matrix
	labels_onehot = (np.arange(NUM_LABELS) == labels_np[:, None]).astype(np.float32)

	return fvecs_np, labels_onehot



def main(argv=None):

	x = tf.placeholder('float', shape=[None, num_features])
	y = tf.placeholder('float', shape=[None, num_labels])
 